
from vavabot_arbitrage_beta_1_1 import Deribit, CredentialsSaved
import time
from lists import list_monitor_log
import threading

connect = Deribit(client_id=CredentialsSaved.api_secret_saved(),
                  client_secret=CredentialsSaved.secret_key_saved(),
                  wss_url=CredentialsSaved.url())

led = 'red'


def led_color():
    led_color1 = led
    return str(led_color1)


def connection():
    global connect
    global led
    while True:
        try:
            connect_set_heartbeat = connect.set_heartbeat()
            if connect_set_heartbeat == 'ok':
                list_monitor_log.append('connection ok')
                led = 'green'
                time.sleep(40)
                pass
            else:
                list_monitor_log.append('********** Thread_connection - Connection ERROR **********')
                led = 'red'
                time.sleep(10)
                connect = Deribit(client_id=CredentialsSaved.api_secret_saved(),
                                  client_secret=CredentialsSaved.secret_key_saved(),
                                  wss_url=CredentialsSaved.url())
        except Exception as e:
            led = 'red'
            time.sleep(10)
            list_monitor_log.append('********** Thread_connection - Connection ERROR ********** ' + str(e))
            pass


run_thread = threading.Thread(daemon=True, target=connection)
run_thread.start()




'''
connect = Deribit(client_id=CredentialsSaved.api_secret_saved(),
                  client_secret=CredentialsSaved.secret_key_saved(),
                  wss_url=CredentialsSaved.url())
'''
'''
def connection(ui):
    def thread_heartbeat():
        from connection_arbitrage import connect
        from lists import list_monitor_log
        green_icon = "./green_led_icon.png"
        red_icon = "./red_led_icon.png"
        while True:
            try:
                connect_set_heartbeat = connect.set_heartbeat()
                if connect_set_heartbeat == 'ok':
                    list_monitor_log.append('connection ok')
                    ui.label_29.setPixmap(QtGui.QPixmap(green_icon))
                    time.sleep(40)
                    pass
                else:
                    list_monitor_log.append('********** Connection ERROR **********')
                    ui.label_29.setPixmap(QtGui.QPixmap(red_icon))
                    time.sleep(10)
                    connect = Deribit(client_id=CredentialsSaved.api_secret_saved(),
                                      client_secret=CredentialsSaved.secret_key_saved(),
                                      wss_url=CredentialsSaved.url())
                    pass
            except Exception as e:
                time.sleep(10)
                list_monitor_log.append('********** Connection ERROR ********** ' + str(e))
                pass

    run_thread = threading.Thread(daemon=True, target=thread_heartbeat)
    run_thread.start()
'''