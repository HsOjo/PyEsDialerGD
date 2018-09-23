import time

from es_dialer_gd import EsDialerGD

client = EsDialerGD()
if client.init():
    print('init success.')
    if client.auth():
        print('auth success.')
        while True:
            try:
                expires = -1
                for i in range(3):
                    expires = client.keep()
                    if expires != -1:
                        break
                    else:
                        print('[%s]keep failed.' % (i + 1))
                time.sleep(expires - 30)
            except:
                import traceback
                traceback.print_exc()
                client.term()
                print('term completed.')
                break
    else:
        print('auth failed.')
else:
    print('init failed.')
    client.term()
    print('term completed.')
