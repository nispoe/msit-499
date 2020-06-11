import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc
import os
import codecs

os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
cert = open(os.path.expanduser('~/.lnd/tls.cert'), 'rb').read()


def create_macaroon(macaroon_path):
    with open(os.path.expanduser(macaroon_path), 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')
    return macaroon

def metadata_callback(context, callback):
    callback([('macaroon', macaroon)], None)

def create_stub(host):
    cert_creds = grpc.ssl_channel_credentials(cert)
    auth_creds = grpc.metadata_call_credentials(metadata_callback)
    combined_creds = grpc.composite_channel_credentials(cert_creds, auth_creds)
    channel = grpc.secure_channel(host, combined_creds)
    stub = lnrpc.LightningStub(channel)
    return stub

alice_macaroon_path ='~/gocode/dev/alice/data/chain/bitcoin/simnet/admin.macaroon'
alice_host = 'localhost:10001'
macaroon = create_macaroon(alice_macaroon_path)
stub_alice = create_stub(alice_host)

response = stub_alice.GetInfo(ln.GetInfoRequest())
print(response)

response = stub_alice.WalletBalance(ln.WalletBalanceRequest())
print('Total Balance = ' + str(response.total_balance))

