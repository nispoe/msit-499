import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc
import os
import codecs

os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
cert = open(os.path.expanduser('~/.lnd/tls.cert'), 'rb').read()
#creds = grpc.ssl_channel_credentials(cert)
#channel = grpc.secure_channel('localhost:10002', creds)
#stub = lnrpc.LightningStub(channel)

with open(os.path.expanduser('~/gocode/dev/bob/data/chain/bitcoin/simnet/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')

#stub.GetInfo(ln.GetInfoRequest(), metadata=[('macaroon', macaroon)])

def metadata_callback(context, callback):
    # for more info see grpc docs
    callback([('macaroon', macaroon)], None)

cert_creds = grpc.ssl_channel_credentials(cert)
auth_creds = grpc.metadata_call_credentials(metadata_callback)
combined_creds = grpc.composite_channel_credentials(cert_creds, auth_creds)
channel = grpc.secure_channel('localhost:10002', combined_creds)
stub = lnrpc.LightningStub(channel)
response = stub.GetInfo(ln.GetInfoRequest())
print(response)

response = stub.WalletBalance(ln.WalletBalanceRequest())
print('Total Balance = ' + str(response.total_balance))

