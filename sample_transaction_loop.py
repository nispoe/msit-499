from datetime import datetime
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
print(response.total_balance)

bob_macaroon_path ='~/gocode/dev/bob/data/chain/bitcoin/simnet/admin.macaroon'
bob_host = 'localhost:10002'
macaroon = create_macaroon(bob_macaroon_path)
stub_bob = create_stub(bob_host)

response = stub_bob.GetInfo(ln.GetInfoRequest())
print(response)

response = stub_bob.WalletBalance(ln.WalletBalanceRequest())
print(response.total_balance)

begin_ts = datetime.now()

for i in range(0,20):
    invoice = ln.Invoice(value=1)
    macaroon = create_macaroon(bob_macaroon_path)
    bobInvoice = stub_bob.AddInvoice(invoice)
    print(bobInvoice.payment_request)

    aliceSendRequest = ln.SendRequest(payment_request=bobInvoice.payment_request)
    macaroon = create_macaroon(alice_macaroon_path)
    aliceSendPayment = stub_alice.SendPaymentSync(aliceSendRequest)
    print(aliceSendPayment)

end_ts = datetime.now()

macaroon = create_macaroon(bob_macaroon_path)
bobListChannels = stub_bob.ListChannels(ln.ListChannelsRequest())
print(bobListChannels)

ts = end_ts - begin_ts
print('Total Time = ' + str(ts))
