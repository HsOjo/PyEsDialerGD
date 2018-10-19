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
                        expires -= 30
                        k += 1
                        print('[%s]keep success. %ds' % (k, expires))
                        break
                    else:
                        print('[%s][%s]keep failed.' % (k, i + 1))
                if expires > 0:
                    time.sleep(expires)
            except KeyboardInterrupt:
                pass
            except:
                traceback.print_exc()
                break
    else:
        print('auth failed.')
else:
    print('init failed.')

client.term()
print('term completed.')
