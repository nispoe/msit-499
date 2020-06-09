from time import sleep
import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc
import os
import codecs

os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
cert = open(os.path.expanduser('./.lnd/tls.cert'), 'rb').read()

with open(os.path.expanduser('~/gocode/dev/alice/data/chain/bitcoin/simnet/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')

def metadata_callback(context, callback):
    callback([('macaroon', macaroon)], None)

cert_creds = grpc.ssl_channel_credentials(cert)
auth_creds = grpc.metadata_call_credentials(metadata_callback)
combined_creds = grpc.composite_channel_credentials(cert_creds, auth_creds)
channel = grpc.secure_channel('localhost:10001', combined_creds)
stub = lnrpc.LightningStub(channel)

def request_generator(dest, amt):
    counter = 0
    print("Starting up")
    while counter < 2:
        request = ln.SendRequest(
            dest=dest,
            amt=amt,
        )
        yield request
        counter += 1
        sleep(2)

# Outputs from lncli are hex-encoded
dest_hex = '028d8e37fb6b34f08b5900df1d4d39e970ff2087bacdf30f43a55905423563c3e0'
dest_bytes = codecs.decode(dest_hex, 'hex')

request_iterable = request_generator(dest=dest_bytes, amt=100)

for payment in stub.SendPayment(request_iterable):
    print(payment)
