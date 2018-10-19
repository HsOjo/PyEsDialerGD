import time
import traceback

from es_dialer_gd import EsDialerGD

client = EsDialerGD()
if client.init():
    print('init success.')
    if client.auth():
        print('auth success.')
        k = 0
        while True:
            try:
                expires = -1
                for i in range(3):
                    expires = client.keep()
                    if expires != -1:
                        k += 1
                        print('[%s]keep success. %ds' % (k, expires - 30))
                        break
                    else:
                        print('[%s]keep failed.' % (i + 1))
                time.sleep(expires - 30)
            except KeyboardInterrupt:
                pass
            except:
                traceback.print_exc()
            finally:
                client.term()
                print('term completed.')
                break
    else:
        print('auth failed.')
else:
    print('init failed.')
    client.term()
    print('term completed.')
