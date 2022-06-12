from gui_arbitrage import *
from connection_arbitrage import *
from websocket import create_connection
from datetime import datetime
import json
import hmac
import hashlib
import time
import threading
global index_greeks_print_on_off
global strategy_on_off
global list_monitor_log
global what_instrument


# Classe de Sinais.
class Sinais(QtCore.QObject):
    # Elementos.
    ui_signal1 = QtCore.pyqtSignal(dict)

    def __init__(self):
        QtCore.QObject.__init__(self)


sinal = Sinais()  # Instância da Classe Sinais.


class CredentialsSaved:
    def __init__(self):
        self.self = self

    @staticmethod
    def api_secret_saved():
        from lists import list_monitor_log
        with open('api-key_arbitrage.txt', 'r') as api_secret_saved_file:
            api_secret_saved_file_read = str(api_secret_saved_file.read())
        list_monitor_log.append('*** API key: ' + str(api_secret_saved_file_read) + ' ***')
        return api_secret_saved_file_read

    @staticmethod
    def secret_key_saved():
        from lists import list_monitor_log
        with open('secret-key_arbitrage.txt', 'r') as secret_key_saved_file:
            secret_key_saved_file_read = str(secret_key_saved_file.read())
        list_monitor_log.append('*** SECRET key: ' + str(secret_key_saved_file_read) + ' ***')
        return secret_key_saved_file_read

    @staticmethod
    def testnet_saved_tru_or_false():
        from lists import list_monitor_log
        with open('testnet_true_or_false_arbitrage.txt', 'r') as testnet_saved_tru_or_false_file:
            testnet_saved_tru_or_false_file_read = str(testnet_saved_tru_or_false_file.read())
        if testnet_saved_tru_or_false_file_read == 'True':
            list_monitor_log.append('*** TEST Account ***')
            return True
        elif testnet_saved_tru_or_false_file_read == 'False':
            list_monitor_log.append('*** REAL Account ***')
            return False
        else:
            list_monitor_log.append('***** ERROR in testnet_saved_tru_or_false *****')

    @staticmethod
    def url():
        from lists import list_monitor_log
        if CredentialsSaved.testnet_saved_tru_or_false() is True:
            list_monitor_log.append('*** URL: ' + 'wss://test.deribit.com/ws/api/v2' + ' ***')
            return 'wss://test.deribit.com/ws/api/v2'
        elif CredentialsSaved.testnet_saved_tru_or_false() is False:
            list_monitor_log.append('*** URL: ' + 'wss://deribit.com/ws/api/v2' + ' ***')
            return 'wss://deribit.com/ws/api/v2'
        else:
            list_monitor_log.append('***** URL ERROR in testnet True or False *****')


class ConfigAndInstrumentsSaved:
    def __init__(self):
        self.self = self
        self.instrument_number = None

    @staticmethod
    def instruments_check():
        with open('instruments_arbitrage.txt', 'r') as instruments_check_file:
            return str(instruments_check_file.read())

    @staticmethod
    def config_check():
        with open('targets_arbitrage.txt', 'r') as config_check_file:
            return str(config_check_file.read())

    def instrument_name_construction_from_file(self, instrument_number=None):
        file_open = 'instruments_arbitrage.txt'
        self.instrument_number = instrument_number

        instrument_number_adjusted_to_list = (int(instrument_number) - 1)

        # open file instruments

        with open(file_open, 'r') as file_instruments:
            lines_file_instruments = file_instruments.readlines()  # file instruments.txt ==> lines
            # Instrument
            list_line_instrument = lines_file_instruments[instrument_number_adjusted_to_list].split()  # line ==> list
            instrument_name = str(list_line_instrument[3])
            return instrument_name

    def instrument_available(self, instrument_number=None):
        from lists import list_monitor_log
        from connection_arbitrage import connect

        self.instrument_number = instrument_number

        instrument_name = ConfigAndInstrumentsSaved().instrument_name_construction_from_file(
            instrument_number=instrument_number)

        currency = str
        if 'BTC' in instrument_name:
            currency = 'BTC'
        elif 'ETH' in instrument_name:
            currency = 'ETH'
        else:
            list_monitor_log.append('********** Instrument currency ERROR in line 106 *********')

        a10 = connect.get_instruments(currency)
        list_instrument_name = []
        for i in a10:
            list_instrument_name.append(i['instrument_name'])
        if instrument_name in list_instrument_name:
            list_instrument_name.clear()
            time.sleep(0.3)
            return 'instrument available'
        else:
            list_instrument_name.clear()
            time.sleep(0.3)
            return 'instrument NO available'

    def instrument_buy_or_sell(self, instrument_number=None):
        file_open = 'instruments_arbitrage.txt'
        self.instrument_number = instrument_number
        instrument_number_adjusted_to_list = (int(instrument_number) - 1)
        with open(file_open, 'r') as file_instruments:
            lines_file_instruments = file_instruments.readlines()  # file instruments.txt ==> lines
            # Instrument
            list_line_instrument = lines_file_instruments[instrument_number_adjusted_to_list].split()  # line ==> list
            instrument_buy_or_sell = str(list_line_instrument[4])
            return instrument_buy_or_sell

    @staticmethod
    def total_amount_saved():
        with open('targets_arbitrage.txt', 'r') as total_amount_saved_file:
            lines_total_amount_saved_file = total_amount_saved_file.readlines()
            list_lines_total_amount_saved_file = lines_total_amount_saved_file[0].split()
            total_amount = str(list_lines_total_amount_saved_file[3])
            return str(total_amount)

    @staticmethod
    def positions_with_same_size_in():
        with open('targets_arbitrage.txt', 'r') as positions_with_same_size_in_file:
            lines_positions_with_same_size_in_file = positions_with_same_size_in_file.readlines()
            list_lines_positions_with_same_size_in_file = lines_positions_with_same_size_in_file[1].split()
            positions_with_same_size_in = str(list_lines_positions_with_same_size_in_file[5])
            return str(positions_with_same_size_in)

    @staticmethod
    def set_entry_position_in():
        with open('targets_arbitrage.txt', 'r') as a_file:
            lines_a_file = a_file.readlines()
            list_lines_a_file = lines_a_file[2].split()
            set_entry_position_in = str(list_lines_a_file[2])
            return str(set_entry_position_in)

    @staticmethod
    def set_entry_position_bigger_lower():
        with open('targets_arbitrage.txt', 'r') as a_file:
            lines_a_file = a_file.readlines()
            list_lines_a_file = lines_a_file[2].split()
            set_entry_position_bigger_lower = str(list_lines_a_file[3])
            return str(set_entry_position_bigger_lower)

    @staticmethod
    def set_entry_position_value():
        with open('targets_arbitrage.txt', 'r') as a_file:
            lines_a_file = a_file.readlines()
            list_lines_a_file = lines_a_file[2].split()
            set_entry_position_value = str(list_lines_a_file[4])
            return str(set_entry_position_value)

    @staticmethod
    def set_exit_position_in():
        with open('targets_arbitrage.txt', 'r') as a_file:
            lines_a_file = a_file.readlines()
            list_lines_a_file = lines_a_file[3].split()
            set_entry_position_in_a = str(list_lines_a_file[0])
            if set_entry_position_in_a == 'Profit':
                a1 = 'Profit'
            else:
                a1 = 'Difference'
            set_entry_position_in = str(str(a1) + '_' + str(list_lines_a_file[2]))
            return set_entry_position_in

    @staticmethod
    def set_exit_position_bigger_lower():
        with open('targets_arbitrage.txt', 'r') as a_file:
            lines_a_file = a_file.readlines()
            list_lines_a_file = lines_a_file[3].split()
            set_exit_position_bigger_lower = str(list_lines_a_file[3])
            return str(set_exit_position_bigger_lower)

    @staticmethod
    def set_exit_position_value():
        with open('targets_arbitrage.txt', 'r') as a_file:
            lines_a_file = a_file.readlines()
            list_lines_a_file = lines_a_file[3].split()
            set_exit_position_value = str(list_lines_a_file[4])
            return str(set_exit_position_value)

    @staticmethod
    def set_stop_loss_in():
        with open('targets_arbitrage.txt', 'r') as a_file:
            lines_a_file = a_file.readlines()
            list_lines_a_file = lines_a_file[4].split()
            set_stop_loss_in = str(list_lines_a_file[2])
            return str(set_stop_loss_in)

    @staticmethod
    def set_stop_loss_value():
        with open('targets_arbitrage.txt', 'r') as a_file:
            lines_a_file = a_file.readlines()
            list_lines_a_file = lines_a_file[4].split()
            set_stop_loss_value = str(list_lines_a_file[3])
            return str(set_stop_loss_value)


class Deribit:
    def __init__(self, client_id=None, client_secret=None, wss_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.wss_url = wss_url

        self._auth(client_id=client_id, wss_url=wss_url, client_secret=client_secret)

    # noinspection PyMethodMayBeStatic
    def logwriter(self, msg):
        from lists import list_monitor_log
        out = datetime.now().strftime("\n[%Y%m%d,%H:%M:%S] ") + str(msg)
        list_monitor_log.append(str(out))
        with open('log_arbitrage.log', 'a') as log_file:
            log_file.write(out)

    def _auth(self, client_id=None, wss_url=None, client_secret=None):
        self.client_id = client_id
        self.wss_url = wss_url
        self.client_secret = client_secret

        from lists import list_monitor_log

        timestamp = round(datetime.now().timestamp() * 1000)
        nonce = "abcd"
        data = ""
        signature = hmac.new(
            bytes(client_secret, "latin-1"),
            msg=bytes('{}\n{}\n{}'.format(timestamp, nonce, data), "latin-1"),
            digestmod=hashlib.sha256
        ).hexdigest().lower()

        try:
            self._WSS = create_connection(wss_url)
            msg = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "public/auth",
                "params": {
                    "grant_type": "client_signature",
                    "client_id": client_id,
                    "timestamp": timestamp,
                    "signature": signature,
                    "nonce": nonce,
                    "data": data
                }
            }
            self.logwriter('Auth OK\n############')
            list_monitor_log.append('identified')
            # print('identified')
            return self._sender(msg)
        except Exception as er:
            self.logwriter('auth error:' + str(er))
            list_monitor_log.append('auth error:' + str(er))

    def _sender(self, msg):
        from lists import list_monitor_log
        try:
            self.logwriter(msg['method'])
            self._WSS.send(json.dumps(msg))
            out = json.loads(self._WSS.recv())
            # logwriter(msg=out['result'])
            # print(out)
            # print(out['result'])
            if 'error' in out:
                self.logwriter(out['error'])
                return out['result']
            else:
                return out['result']
        except Exception as er:
            self.logwriter('_sender error: ' + str(er))
            list_monitor_log.append('_sender error: ' + str(er))

    def get_instruments(self, currency):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "public/get_instruments",
                "params": {
                    "currency": currency,
                    # "kind": "future",
                    "expired": False
                }
            }
        return self._sender(msg)

    def index_price(self, currency):
        msg = \
            {
                "jsonrpc": "2.0",
                "method": "public/get_index_price",
                "id": 3,
                "params": {
                    "index_name": currency
                }
             }
        return self._sender(msg)

    def set_heartbeat(self):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "public/set_heartbeat",
                "params": {
                    "interval": 60
                }
            }
        return self._sender(msg)

    def disable_heartbeat(self):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "public/disable_heartbeat",
                "params": {

                }
            }
        return self._sender(msg)

    def get_position(self, instrument_name=None):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "private/get_position",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def get_order_book(self, instrument_name=None):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 7,
                "method": "public/get_order_book",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def buy_limit(self, currency, amount, price):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 8,
                "method": "private/buy",
                "params": {
                    "instrument_name": currency,
                    "amount": amount,
                    "type": "limit",
                    "price": price
                }
            }
        return self._sender(msg)

    def sell_limit(self, currency, amount, price):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 9,
                "method": "private/sell",
                "params": {
                    "instrument_name": currency,
                    "amount": amount,
                    "type": "limit",
                    "price": price
                }
            }
        return self._sender(msg)

    def buy_pos_only(self, currency, amount, price):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 10,
                "method": "private/buy",
                "params": {
                    "instrument_name": currency,
                    "amount": amount,
                    "price": price,
                    "post_only": True
                }
            }
        return self._sender(msg)

    def sell_pos_only(self, currency, amount, price):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 11,
                "method": "private/sell",
                "params": {
                    "instrument_name": currency,
                    "amount": amount,
                    "price": price,
                    "post_only": True
                }
            }
        return self._sender(msg)

    def buy_market(self, currency, amount):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 12,
                "method": "private/buy",
                "params": {
                    "instrument_name": currency,
                    "amount": amount,
                    "type": "market"
                }
            }
        return self._sender(msg)

    def sell_market(self, currency, amount):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 13,
                "method": "private/sell",
                "params": {
                    "instrument_name": currency,
                    "amount": amount,
                    "type": "market"
                }
            }
        return self._sender(msg)

    def cancel_all(self):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 14,
                "method": "private/cancel_all",
                "params": {

                }
            }
        return self._sender(msg)

    def get_instruments_future(self, currency):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 15,
                "method": "public/get_instruments",
                "params": {
                    "currency": currency,
                    "kind": "future",
                    "expired": False
                }
            }
        return self._sender(msg)

    def get_book_summary_by_instrument(self, instrument_name):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 16,
                "method": "public/get_book_summary_by_instrument",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def close_position(self, instrument_name):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 17,
                "method": "private/close_position",
                "params": {
                    "instrument_name": instrument_name,
                    "type": "market"
                }
            }
        return self._sender(msg)


def credentials(ui):
    def message_box_reboot():
        import sys

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('If you update\nAPI key and secret key\nyou will need restart bot')
        msg.setWindowTitle('*** WARNING ***')
        msg.addButton('Ok', msg.AcceptRole)
        msg.addButton('Cancel', msg.RejectRole)
        pass
        if msg.exec_() == msg.Rejected:
            api_key_save()  # ok clicked
            time.sleep(1)
            sys.exit()
        else:
            pass  # cancel clicked

    def message_box_reboot1():
        if CredentialsSaved.testnet_saved_tru_or_false() == '':
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('You need\nSet Test or Real Account')
            msg.setWindowTitle('INFO')
            msg.exec_()
            pass
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Test or Real Account\nIs Correct?')
            msg.setWindowTitle('*** WARNING ***')
            msg.addButton('Yes', msg.AcceptRole)
            msg.addButton('No', msg.RejectRole)
            pass
            if msg.exec_() == msg.Rejected:
                message_box_reboot()  # ok clicked
            else:
                pass  # cancel clicked

    def message_box_reboot2():
        import sys
        if CredentialsSaved.testnet_saved_tru_or_false() is True:
            pass
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Dou you want\nUpdate Account? ')
            msg.setWindowTitle('*** WARNING ***')
            msg.addButton('Yes', msg.AcceptRole)
            msg.addButton('No', msg.RejectRole)
            pass
            if msg.exec_() == msg.Rejected:
                testnet_true_save()  # ok clicked

                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Dou you want\nUpdate APIs? ')
                msg.setWindowTitle('*** WARNING ***')
                msg.addButton('Yes', msg.AcceptRole)
                msg.addButton('No', msg.RejectRole)
                pass
                if msg.exec_() == msg.Rejected:
                    message_box_reboot()  # ok clicked
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText('You need\nRestart bot')
                    msg.setWindowTitle('INFO')
                    msg.exec_()
                    pass  # cancel clicked
                    sys.exit()
            else:
                if CredentialsSaved.testnet_saved_tru_or_false() is True:
                    ui.radioButton_testnet_true.setChecked(True)
                    ui.radioButton_2_testnet_false.setChecked(False)
                elif CredentialsSaved.testnet_saved_tru_or_false() is False:
                    ui.radioButton_testnet_true.setChecked(False)
                    ui.radioButton_2_testnet_false.setChecked(True)
                else:
                    ui.radioButton_testnet_true.setChecked(False)
                    ui.radioButton_2_testnet_false.setChecked(False)
                    pass  # cancel clicked

    def message_box_reboot3():
        import sys
        if CredentialsSaved.testnet_saved_tru_or_false() is False:
            pass
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Dou you want\nUpdate Account? ')
            msg.setWindowTitle('*** WARNING ***')
            msg.addButton('Yes', msg.AcceptRole)
            msg.addButton('No', msg.RejectRole)
            pass
            if msg.exec_() == msg.Rejected:
                testnet_false_save()  # ok clicked

                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Dou you want\nUpdate APIs? ')
                msg.setWindowTitle('*** WARNING ***')
                msg.addButton('Yes', msg.AcceptRole)
                msg.addButton('No', msg.RejectRole)
                pass
                if msg.exec_() == msg.Rejected:
                    message_box_reboot()  # ok clicked
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText('You need\nRestart bot')
                    msg.setWindowTitle('INFO')
                    msg.exec_()
                    pass  # cancel clicked
                    sys.exit()
            else:
                if CredentialsSaved.testnet_saved_tru_or_false() is True:
                    ui.radioButton_testnet_true.setChecked(True)
                    ui.radioButton_2_testnet_false.setChecked(False)
                elif CredentialsSaved.testnet_saved_tru_or_false() is False:
                    ui.radioButton_testnet_true.setChecked(False)
                    ui.radioButton_2_testnet_false.setChecked(True)
                else:
                    ui.radioButton_testnet_true.setChecked(False)
                    ui.radioButton_2_testnet_false.setChecked(False)
                    pass  # cancel clicked

    def api_key_saved_print():
        ui.lineEdit_api_key_saved.setText(CredentialsSaved.api_secret_saved())

    def secret_key_saved_print():
        ui.lineEdit_api_secret_saved.setText(CredentialsSaved.secret_key_saved())

    def testnet_true_or_false_saved_print():
        testnet_true_or_false_saved_print_file = CredentialsSaved.testnet_saved_tru_or_false()
        if testnet_true_or_false_saved_print_file is True:
            ui.lineEdit_testenet_true_or_false_satatus.setText('Test Account')
            ui.radioButton_testnet_true.setChecked(True)
            ui.radioButton_2_testnet_false.setChecked(False)
        elif testnet_true_or_false_saved_print_file is False:
            ui.lineEdit_testenet_true_or_false_satatus.setText('Real Account')
            ui.radioButton_testnet_true.setChecked(False)
            ui.radioButton_2_testnet_false.setChecked(True)
        else:
            ui.lineEdit_testenet_true_or_false_satatus.setText('SET Account')
            ui.radioButton_testnet_true.setChecked(False)
            ui.radioButton_2_testnet_false.setChecked(False)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('You need\nSet Test or Real Account')
            msg.setWindowTitle('*** Warning ***')
            msg.exec_()
            pass

    def api_key_save():
        with open('api-key_arbitrage.txt', 'w') as api_key_save_file:
            api_key_save_file.write(str(ui.lineEdit_api_key_new.text()))
        secret_key_save()
        api_key_saved_print()

    def secret_key_save():
        with open('secret-key_arbitrage.txt', 'w') as secret_key_save_file:
            secret_key_save_file.write(str(ui.lineEdit_api_secret_new.text()))
        secret_key_saved_print()

    def testnet_true_save():
        with open('testnet_true_or_false_arbitrage.txt', 'w') as testnet_true_save_file:
            testnet_true_save_file.write('True')
        testnet_true_or_false_saved_print()

    def testnet_false_save():
        with open('testnet_true_or_false_arbitrage.txt', 'w') as testnet_false_save_file:
            testnet_false_save_file.write('False')
        testnet_true_or_false_saved_print()

    api_key_saved_print()
    secret_key_saved_print()
    testnet_true_or_false_saved_print()
    ui.pushButton_submit_new_credintals.clicked.connect(message_box_reboot1)
    ui.radioButton_testnet_true.clicked.connect(message_box_reboot2)
    ui.radioButton_2_testnet_false.clicked.connect(message_box_reboot3)


def config(ui):
    def set_date():
        date_now_instrument = QtCore.QDate.currentDate()
        ui.lineEdit_maturity_instrumet1.setDate(date_now_instrument.addDays(-1))
        ui.lineEdit_maturity_instrumet1_2.setDate(date_now_instrument.addDays(-1))
    def remove_log_arbitrage_log_if_bigger_500kb_when_open_app():
        import os
        from lists import list_monitor_log

        try:
            if os.path.isfile('log_arbitrage.log') is True:
                if float(os.path.getsize('log_arbitrage.log')) > 500000:
                    os.unlink('log_arbitrage.log')
                else:
                    pass
            else:
                pass

        except Exception as er:
            list_monitor_log.append('***** ERROR in remove_log_arbitrage_log_if_bigger_500kb_when_open_app():' +
                                    str(er) + '. Error Code 713 *****')

    def enable_disable_maturity():
        ui.lineEdit_o_or_f_instrumet1.setCurrentText('Future')
        ui.lineEdit_o_or_f_instrumet1.setEnabled(False)
        ui.lineEdit_o_or_f_instrumet1_2.setCurrentText('Future')
        ui.lineEdit_o_or_f_instrumet1_2.setEnabled(False)

    def instruments_saved_print_and_check_available():
        from lists import list_monitor_log
        ui.textEdit_instruments_saved.setText(ConfigAndInstrumentsSaved.instruments_check())
        try:
            if ConfigAndInstrumentsSaved().instrument_available(instrument_number=1) == 'instrument available' and \
                    ConfigAndInstrumentsSaved().instrument_available(instrument_number=2) == 'instrument available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instruments Syntax OK')
                msg.setWindowTitle('INFO')
                msg.exec_()
                pass
            elif ConfigAndInstrumentsSaved().instrument_available(instrument_number=1) == 'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 1 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            elif ConfigAndInstrumentsSaved().instrument_available(instrument_number=2) == 'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 2 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instruments Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
        except Exception as er:
            list_monitor_log.append(str(er))
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Instruments Syntax ERROR')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass

    def config_saved_print():
        ui.textEdit_instruments_saved_2.setText(ConfigAndInstrumentsSaved.config_check())

    def instruments_save():
        from lists import list_monitor_log
        try:
            date_now_instrument = QtCore.QDate.currentDate()
            if ui.lineEdit_currency_instrumet1.currentText() == 'Set BTC or ETH:' or \
                    ui.lineEdit_currency_instrumet1_2.currentText() == 'Set BTC or ETH:':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('All fields are required - ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass

            elif ui.lineEdit_o_or_f_instrumet1_3.currentText() == ui.lineEdit_o_or_f_instrumet1_4.currentText():
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instruments directions (buy/sell)\nmust be\nDifferent\n   ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass

            elif ui.checkBox_perpetual_1.isChecked() and ui.checkBox_perpetual_2.isChecked():
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instruments maturities\nmust be\nDifferent\n   ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass

            elif ui.lineEdit_maturity_instrumet1.text() == ui.lineEdit_maturity_instrumet1_2.text() and \
                    ui.checkBox_perpetual_1.checkState() == 0 and ui.checkBox_perpetual_2.checkState() == 0:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instruments maturities\nmust be\nDifferent\n   ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass

            elif ui.lineEdit_currency_instrumet1.currentText() != ui.lineEdit_currency_instrumet1_2.currentText():
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instruments currencies\nmust be\nsame currency\n   ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass

            elif ui.lineEdit_maturity_instrumet1.currentText() == lineEdit_maturity_instrumet1_2.addDays(-1) or \
                    ui.lineEdit_currency_instrumet1_2.currentText() == date_now_instrument.addDays(-1):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instruments maturities\nmust be set\n   ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass

            elif (ui.lineEdit_currency_instrumet1.currentText() == 'BTC' or
                  ui.lineEdit_currency_instrumet1.currentText() == 'ETH') and \
                (ui.lineEdit_currency_instrumet1_2.currentText() == 'BTC' or
                 ui.lineEdit_currency_instrumet1_2.currentText() == 'BTC'):
                if ui.checkBox_perpetual_1.isChecked():
                    instrument1_to_save = str(
                        'Instrument 1: ' +
                        str(ui.lineEdit_o_or_f_instrumet1.currentText()) + ' ' +
                        str(ui.lineEdit_currency_instrumet1.currentText()) + '-' +
                        'PERPETUAL' + ' ' +
                        str(ui.lineEdit_o_or_f_instrumet1_3.currentText().lower())
                    )
                else:
                    instrument1_to_save = str(
                        'Instrument 1: ' +
                        str(ui.lineEdit_o_or_f_instrumet1.currentText()) + ' ' +
                        str(ui.lineEdit_currency_instrumet1.currentText()) + '-' +
                        str(ui.lineEdit_maturity_instrumet1.text().upper()) + ' ' +
                        str(ui.lineEdit_o_or_f_instrumet1_3.currentText().lower())
                    )
                    pass

                if ui.checkBox_perpetual_2.isChecked():
                    instrument2_to_save = str(
                        'Instrument 2: ' +
                        str(ui.lineEdit_o_or_f_instrumet1_2.currentText()) + ' ' +
                        str(ui.lineEdit_currency_instrumet1_2.currentText()) + '-' +
                        'PERPETUAL' + ' ' +
                        str(ui.lineEdit_o_or_f_instrumet1_4.currentText().lower())
                    )
                    pass
                else:
                    instrument2_to_save = str(
                        'Instrument 2: ' +
                        str(ui.lineEdit_o_or_f_instrumet1_2.currentText()) + ' ' +
                        str(ui.lineEdit_currency_instrumet1_2.currentText()) + '-' +
                        str(ui.lineEdit_maturity_instrumet1_2.text().upper()) + ' ' +
                        str(ui.lineEdit_o_or_f_instrumet1_4.currentText().lower())
                    )
                    pass

                with open('instruments_arbitrage.txt', 'w') as instruments_save_file:
                    instruments_save_file.write(str(instrument1_to_save) + '\n' + str(instrument2_to_save))
                instruments_saved_print_and_check_available()
            else:
                pass
        except Exception as er:
            list_monitor_log.append(str(er))
            instruments_save_file.close()

        ui.pushButton_submit_new_credintals.setEnabled(False)
        ui.radioButton_testnet_true.setEnabled(False)
        ui.radioButton_2_testnet_false.setEnabled(False)

    def disable_positions_with_same_size_in():
        ui.lineEdit_o_or_f_instrumet1_5.setDisabled(True)

    def config_save():
        from lists import list_monitor_log
        try:
            if ui.lineEdit_o_or_f_instrumet1_9.currentText() == 'Set Entry Position' or \
                    ui.lineEdit_o_or_f_instrumet1_8.currentText() == 'Set Exit Position' or \
                    ui.lineEdit_o_or_f_instrumet1_10.currentText() == 'Set Stop Loss':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('All fields are required - ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                with open('targets_arbitrage.txt', 'w') as config_save_file:
                    config_save_file.write(
                        str(ui.label_9.text()) + ' ' + str(
                            ui.lineEdit_currency_exchange_rate_for_upper_and_lower1_2.text()) +
                        '\n' + str(ui.label_6.text()) + ' ' + str(ui.lineEdit_o_or_f_instrumet1_5.currentText()) +
                        '\n' + str(ui.lineEdit_o_or_f_instrumet1_9.currentText()) + str.replace(str(
                            ui.lineEdit_currency_exchange_rate_upper1_2.text()), ',', '.') +
                        '\n' + str(ui.lineEdit_o_or_f_instrumet1_8.currentText()) + str.replace(str(
                            ui.lineEdit_currency_exchange_rate_lower1_3.text()), ',', '.') +
                        '\n' + str.replace(str(ui.lineEdit_o_or_f_instrumet1_10.currentText()), ' (Loss)', '') +
                        ': ' + str.replace(str(ui.lineEdit_currency_exchange_rate_lower1_4.text()), ',', '.')
                    )
                config_saved_print()
        except Exception as er:
            list_monitor_log.append(str(er))
            config_save_file.close()

    remove_log_arbitrage_log_if_bigger_500kb_when_open_app()
    set_date()
    enable_disable_maturity()
    instruments_saved_print_and_check_available()
    config_saved_print()
    ui.pushButton_submit_new_instruments.clicked.connect(instruments_save)
    ui.pushButton_submit_new_instruments_2.clicked.connect(config_save)
    disable_positions_with_same_size_in()


def run_arbitrage(ui):
    from lists import list_monitor_log

    def ui_signal1(info):
        object_signal = info['object_signal']

        if object_signal == 'led_connection':
            led_color1 = str(info['led_color'])
            if led_color1 == 'green':
                green_icon = "./green_led_icon.png"
                ui.label_29.setPixmap(QtGui.QPixmap(green_icon))
            elif led_color1 == 'red':
                red_icon = "./red_led_icon.png"
                ui.label_29.setPixmap(QtGui.QPixmap(red_icon))
            else:
                pass

        elif object_signal == 'textedit_monitor_append':
            msg1 = str(info['msg'])
            ui.textEdit_monitor.append(msg1)

        elif object_signal == 'pushbutton_2_click_signal':
            ui.textEdit_monitor.clear()

        elif object_signal == 'checkBox_autoScrollBar':
            if info['msg'] is True:
                ui.textEdit_monitor.verticalScrollBar().setValue(999999)
            else:
                ui.textEdit_monitor.verticalScrollBar()

        elif object_signal == 'lineEdit_58':
            ui.lineEdit_58.setText(str(info['msg']))

        elif object_signal == 'btc_index_and_greeks_structure_monitor_print':
            b = str(info['msg']['lineEdit_24_btc_index'])
            ui.lineEdit_24_btc_index.setText(b)

            instrument1_name_for_monitor = str(info['msg']['lineEdit'])
            ui.lineEdit.setText(str(instrument1_name_for_monitor))

            c = info['msg']['c']

            d = str(round(c['mark_price'], 2))
            ui.lineEdit_25.setText(d)

            g = str(c['direction'])
            ui.lineEdit_5.setText(g)

            h = str(round(c['average_price'], 2))
            ui.lineEdit_4.setText(h)

            j = str(round(c['size'], 2))
            ui.lineEdit_24.setText(j)

            k = str(round(c['size_currency'], 4))
            ui.lineEdit_26.setText(k)

            m = str(round(c['total_profit_loss'], 4))
            ui.lineEdit_27.setText(m)

            n = str(round(c['leverage'], 2))
            ui.lineEdit_2.setText(n)

            if str(c['estimated_liquidation_price']) == 'None':
                o = 'None'
            else:
                o = str(round(c['estimated_liquidation_price'], 2))
            ui.lineEdit_3.setText(o)

            ui.lineEdit_11.setText(str(info['msg']['lineEdit_11']))
            ui.lineEdit_32.setText(str(info['msg']['lineEdit_32']))

            if str(info['msg']['lineEdit_32']) == 'No bid/ask offer':
                pass
            else:
                ui.lineEdit_6.setText(str(info['msg']['lineEdit_6']))

                c2 = info['msg']['c2']

                d2 = str(round(c2['mark_price'], 2))
                ui.lineEdit_30.setText(d2)

                g2 = str(c2['direction'])
                ui.lineEdit_10.setText(g2)

                h2 = str(round(c2['average_price'], 2))
                ui.lineEdit_9.setText(h2)

                j2 = str(round(c2['size'], 2))
                ui.lineEdit_28.setText(j2)

                k2 = str(round(c2['size_currency'], 4))
                ui.lineEdit_29.setText(k2)

                m2 = str(round(c2['total_profit_loss'], 4))
                ui.lineEdit_31.setText(m2)

                n2 = str(round(c2['leverage'], 2))
                ui.lineEdit_7.setText(n2)

                if str(c2['estimated_liquidation_price']) == 'None':
                    o2 = 'None'
                else:
                    o2 = str(round(c2['estimated_liquidation_price'], 2))
                ui.lineEdit_8.setText(o2)

                ui.lineEdit_12.setText(str(info['msg']['lineEdit_12']))
                p2 = str(info['msg']['lineEdit_33'])
                ui.lineEdit_33.setText(p2)

                ui.lineEdit_34.setText(str(info['msg']['lineEdit_34']))
                ui.lineEdit_35.setText(str(info['msg']['lineEdit_35']))
                ui.lineEdit_36.setText(str(info['msg']['lineEdit_36']))

        elif object_signal == 'setup_arbitrage_strategy_started':
            ui.pushButton_stop_arbitrage.setEnabled(True)
            ui.lineEdit_api_key_new.setEnabled(False)
            ui.lineEdit_api_secret_new.setEnabled(False)
            ui.pushButton_submit_new_credintals.setEnabled(False)
            ui.radioButton_testnet_true.setEnabled(False)
            ui.radioButton_2_testnet_false.setEnabled(False)
            ui.pushButton_submit_new_instruments.setEnabled(False)
            ui.pushButton_submit_new_instruments_2.setEnabled(False)
            ui.pushButton.setText('Arbitrage\nStarted')
            ui.pushButton.setEnabled(False)
            ui.pushButton_start_trading.setEnabled(False)
            ui.lineEdit_58.hide()

            green_icon = "./green_led_icon.png"
            ui.label_32.setPixmap(QtGui.QPixmap(green_icon))

        elif object_signal == 'setup_arbitrage_strategy_stopped':
            ui.pushButton_stop_arbitrage.setEnabled(False)
            ui.lineEdit_api_key_new.setEnabled(True)
            ui.lineEdit_api_secret_new.setEnabled(True)
            ui.pushButton_submit_new_credintals.setEnabled(True)
            ui.radioButton_testnet_true.setEnabled(True)
            ui.radioButton_2_testnet_false.setEnabled(True)
            ui.pushButton_submit_new_instruments.setEnabled(True)
            ui.pushButton_submit_new_instruments_2.setEnabled(True)
            ui.pushButton.setText('Chronometer\nEnabled')
            ui.pushButton.setEnabled(False)
            ui.pushButton_start_trading.setEnabled(True)
            ui.lineEdit_58.show()

            red_icon = "./red_led_icon.png"
            ui.label_32.setPixmap(QtGui.QPixmap(red_icon))

        elif object_signal == 'setup_gui_for_print_index_and_summary':
            red_icon = "./red_led_icon.png"
            ui.label_32.setPixmap(QtGui.QPixmap(red_icon))

            ui.pushButton_stop_arbitrage.setEnabled(False)
            ui.pushButton.setEnabled(False)
            ui.pushButton.setText('Chronometer\nEnabled')

        else:
            pass

    def lists_monitor():
        import time
        from lists import list_monitor_log, list_monitor_print_log
        from connection_arbitrage import connect

        counter = 0
        len_log_a = 0
        led1 = led_color()

        if led1 == 'green':
            info = {'object_signal': 'led_connection', 'led_color': 'green'}
            sinal.ui_signal1.emit(info)
        elif led1 == 'red':
            info = {'object_signal': 'led_connection', 'led_color': 'red'}
            sinal.ui_signal1.emit(info)
        else:
            connect.logwriter('*** ERROR - lists_monitor() Error Code:: 922 ***')
            msg2 = str('*** ERROR - lists_monitor() Error Code:: 923 ***')
            info = {'object_signal': 'textedit_monitor_append', 'msg': msg2}
            sinal.ui_signal1.emit(info)

        while True:
            try:
                len_log_b = len(list_monitor_log)
                if len_log_a != len_log_b:
                    list_monitor_print_log.append(list_monitor_log[len_log_a:])
                    del (list_monitor_log[:len_log_a])
                    for i in range(len(list_monitor_print_log)):
                        msg3 = str(list_monitor_print_log[i])
                        del (list_monitor_print_log[i])
                        info = {'object_signal': 'textedit_monitor_append', 'msg': msg3}
                        sinal.ui_signal1.emit(info)
                    len_log_a = len(list_monitor_log)
                    counter = counter + 1
                    time.sleep(0.0001)
                    pass
                else:
                    time.sleep(0.0001)
                    pass

                if led1 != led_color():
                    if led_color() == 'green':
                        led1 = led_color()
                        info = {'object_signal': 'led_connection', 'led_color': 'green'}
                        sinal.ui_signal1.emit(info)
                    elif led_color() == 'red':
                        led1 = led_color()
                        info = {'object_signal': 'led_connection', 'led_color': 'red'}
                        sinal.ui_signal1.emit(info)
                    else:
                        connect.logwriter('*** ERROR - lists_monitor() Error Code:: 956 ***')
                        msg4 = str('*** ERROR - lists_monitor() Error Code:: 957 ***')
                        info = {'object_signal': 'textedit_monitor_append', 'msg': msg4}
                        sinal.ui_signal1.emit(info)
                        pass
                else:
                    pass

                if counter >= 10000:
                    counter = 0
                    info = {'object_signal': 'pushbutton_2_click_signal', 'msg': ''}
                    sinal.ui_signal1.emit(info)
                    time.sleep(0.5)
                    pass
                else:
                    pass
            except Exception as er:
                from connection_arbitrage import connect
                connect.logwriter(str(er) + ' Error Code:: 975')
                msg5 = str('*** ERROR - lists_monitor() Error Code:: 976: ' + str(er) + ' ***')
                info = {'object_signal': 'textedit_monitor_append', 'msg': msg5}
                sinal.ui_signal1.emit(info)
                time.sleep(5)
            finally:
                pass

    def autoscroll_monitor():
        if ui.checkBox_autoScrollBar.isChecked() is True:
            info = {'object_signal': 'checkBox_autoScrollBar', 'msg': True}
            sinal.ui_signal1.emit(info)
        else:
            info = {'object_signal': 'checkBox_autoScrollBar', 'msg': False}
            sinal.ui_signal1.emit(info)

    def btc_index_and_greeks_structure_monitor_print():
        from lists import list_monitor_log
        try:
            from connection_arbitrage import connect
            a = connect.index_price('btc_usd')
            b = str(round(a['index_price'], 2))

            instrument1_name_for_monitor = str(ConfigAndInstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=1))
            instrument2_name_for_monitor = str(ConfigAndInstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=2))

            c = connect.get_position(instrument_name=str(instrument1_name_for_monitor))

            p_ = annualized_premium(instrument_name=str(instrument1_name_for_monitor))

            if p_ == 'No bid/ask offer':
                msg5 = {
                    'lineEdit_24_btc_index': b,
                    'lineEdit': str(instrument1_name_for_monitor),
                    'c': c,
                    'lineEdit_11': str(str(instrument1_name_for_monitor) + ' An.Premium (%)'),
                    'lineEdit_32': str(p_),
                    'lineEdit_6': '',
                    'c2': '',
                    'lineEdit_12': '',
                    'lineEdit_33': '',
                    'lineEdit_34': '',
                    'lineEdit_35': '',
                    'lineEdit_36': ''
                }
                info5 = {
                    'object_signal': 'btc_index_and_greeks_structure_monitor_print',
                    'msg': msg5
                }
                sinal.ui_signal1.emit(info5)
                pass
            else:
                c2 = connect.get_position(instrument_name=str(instrument2_name_for_monitor))

                p2_ = annualized_premium(instrument_name=str(instrument2_name_for_monitor))
                p2 = str(p2_)

                if p2 == 'No bid/ask offer' or c['mark_price'] == 0.0 or c2['mark_price'] == 0.0:
                    q = str(round((c2['mark_price'] - c['mark_price']), 2))
                    r = 'None'
                    s = 'None'
                    list_monitor_log.append('********** Mark Price is Zero OR No bid/ask offer **********  Mark Price: '
                                            + str(instrument1_name_for_monitor) + ' = ' + str(c['mark_price']) + '     '
                                            + str(instrument2_name_for_monitor) + ' = ' + str(c2['mark_price']))
                    pass
                else:
                    q = str(round((c2['mark_price'] - c['mark_price']), 2))
                    r = str(round(((c2['mark_price'] - c['mark_price']) * 100 / c['mark_price']), 2))
                    s = str(round(float(p2_) - float(p_), 2))

                msg5 = {
                    'lineEdit_24_btc_index': b,  # btc index price
                    'lineEdit': str(instrument1_name_for_monitor),  # Instrument name
                    'c': c,
                    'lineEdit_11': str(str(instrument1_name_for_monitor) + ' An.Premium (%)'),
                    'lineEdit_32': str(p_),
                    'lineEdit_6': str(instrument2_name_for_monitor),
                    'c2': c2,
                    'lineEdit_12': str(str(instrument2_name_for_monitor) + ' An.Premium (%)'),
                    'lineEdit_33': p2,
                    'lineEdit_34': q,
                    'lineEdit_35': r,
                    'lineEdit_36': s
                }
                info5 = {
                    'object_signal': 'btc_index_and_greeks_structure_monitor_print',
                    'msg': msg5
                }
                sinal.ui_signal1.emit(info5)

        except Exception as er:
            list_monitor_log.append(
                '********** btc_index_and_greeks_structure_monitor_print ' + str(er) +
                ' **********'
            )

    def print_index_and_summary():
        global index_greeks_print_on_off
        index_greeks_print_on_off = 'on'

        sinal.ui_signal1.emit({
            'object_signal': 'setup_gui_for_print_index_and_summary',
            'msg': ''
        })

        while index_greeks_print_on_off == 'on':

            btc_index_and_greeks_structure_monitor_print()  # Já tem signal

            for item in range(10, -1, -1):
                sinal.ui_signal1.emit({
                    'object_signal': 'lineEdit_58',
                    'msg': str(item)
                })
                time.sleep(1)

        thread_arbitrage_strategy()

    def number_multiple_10_and_round_0_digits(number=None):
        return round(float(number - (number % 10)), 0)

    def check_instruments_positions(instrument_name_1, instrument_name_2,
                                    positions_with_same_size_in_usd_or_currency,
                                    total_amount,
                                    instrument_buy_or_sell1, instrument_buy_or_sell2
                                    ):
        from connection_arbitrage import connect
        from lists import list_monitor_log

        # Args modifically

        summary_instrument1 = connect.get_position(instrument_name=instrument_name_1)
        summary_instrument2 = connect.get_position(instrument_name=instrument_name_2)

        instrument_position1 = float(summary_instrument1['size'])
        instrument_position2 = float(summary_instrument2['size'])

        order_book_instrument1 = connect.get_order_book(instrument_name=instrument_name_1)
        order_book_instrument2 = connect.get_order_book(instrument_name=instrument_name_2)

        # Args modifically - smaller_amount_dic and instrument_price1 and instrument_price2 - start *******************
        smaller_amount_dic = dict()
        smaller_amount_dic.clear()

        if positions_with_same_size_in_usd_or_currency == 'USD':
            smaller_amount_dic['abs(abs(instrument_position2) - abs(instrument_position1))'] = \
                number_multiple_10_and_round_0_digits(abs(
                    abs(instrument_position2) - abs(instrument_position1)
                ))
        else:
            pass

        if summary_instrument1['direction'] == 'buy' and order_book_instrument1['best_bid_amount'] != 0:
            best_bid_ask_amount1 = float(order_book_instrument1['best_bid_amount'])
            best_bid_ask_price1 = float(order_book_instrument1['best_bid_price'])
        elif summary_instrument1['direction'] == 'sell' and order_book_instrument1['best_ask_amount'] != 0:
            best_bid_ask_amount1 = float(order_book_instrument1['best_ask_amount'])
            best_bid_ask_price1 = float(order_book_instrument1['best_ask_price'])
        else:
            best_bid_ask_amount1 = 0
            best_bid_ask_price1 = 0

        if summary_instrument2['direction'] == 'buy' and order_book_instrument2['best_bid_amount'] != 0:
            best_bid_ask_amount2 = float(order_book_instrument2['best_bid_amount'])
            best_bid_ask_price2 = float(order_book_instrument2['best_bid_price'])
        elif summary_instrument2['direction'] == 'sell' and order_book_instrument2['best_ask_amount'] != 0:
            best_bid_ask_amount2 = float(order_book_instrument2['best_ask_amount'])
            best_bid_ask_price2 = float(order_book_instrument2['best_ask_price'])
        else:
            best_bid_ask_amount2 = 0
            best_bid_ask_price2 = 0

        if abs(instrument_position1) > abs(instrument_position2):
            smaller_amount_dic['best_bid_ask_amount1'] = number_multiple_10_and_round_0_digits(
                abs(float(best_bid_ask_amount1))
            )
        else:
            smaller_amount_dic['best_bid_ask_amount2'] = number_multiple_10_and_round_0_digits(
                abs(float(best_bid_ask_amount2))
            )

        if len(smaller_amount_dic) > 0:
            smaller_amount_name = min(smaller_amount_dic, key=smaller_amount_dic.get)  # name
            smaller_amount = smaller_amount_dic.get(smaller_amount_name, 0)  # Valor
        else:
            smaller_amount = 0  # valor
        # Args modifically - smaller_amount_dic and instrument_price1 and instrument_price2 - the end ******************

        # there_are_bid_ask_offer for instrument1 postirion != instrument2_position - start ****************************
        if number_multiple_10_and_round_0_digits(best_bid_ask_amount1) >= 10 and \
                abs(instrument_position1) > abs(instrument_position2):
            there_are_bid_ask_offer = True
        elif number_multiple_10_and_round_0_digits(best_bid_ask_amount2) >= 10 and \
                abs(instrument_position1) < abs(instrument_position2):
            there_are_bid_ask_offer = True
        elif (number_multiple_10_and_round_0_digits(best_bid_ask_amount1) < 10 and
                abs(instrument_position1) > abs(instrument_position2)) or \
            (number_multiple_10_and_round_0_digits(best_bid_ask_amount2) < 10 and
                abs(instrument_position1) < abs(instrument_position2)):
            there_are_bid_ask_offer = False
            list_monitor_log.append(' ****** There is NO bid or ask offer in Check Instruments Positions ***** ')
            list_monitor_log.append(
                instrument_name_1 + ': ' + str(best_bid_ask_amount1) + ' bid/ask amount ')
            list_monitor_log.append(
                instrument_name_2 + ': ' + str(best_bid_ask_amount2) + ' bid/ask amount ')
        else:
            there_are_bid_ask_offer = False
        # # there_are_bid_ask_offer for instrument1 postirion != instrument2_position - the end ************************

        if positions_with_same_size_in_usd_or_currency == 'USD' and \
                ((instrument_buy_or_sell1 != summary_instrument1['direction'] and summary_instrument1['size'] != 0) or
                 (instrument_buy_or_sell2 != summary_instrument2['direction'] and summary_instrument2['size'] != 0)):

            if instrument_buy_or_sell1 != summary_instrument1['direction'] and summary_instrument1['size'] != 0:
                if best_bid_ask_amount1 <= abs(float(instrument_position1) - 0):
                    amount_for_direction_instrument1 = number_multiple_10_and_round_0_digits(
                        abs(float(best_bid_ask_amount1)))
                else:
                    amount_for_direction_instrument1 = number_multiple_10_and_round_0_digits(
                        abs(float(instrument_position1) - 0))
            else:
                amount_for_direction_instrument1 = 0

            if instrument_buy_or_sell2 != summary_instrument2['direction'] and summary_instrument2['size'] != 0:
                if best_bid_ask_amount2 <= abs(float(instrument_position2) - 0):
                    amount_for_direction_instrument2 = number_multiple_10_and_round_0_digits(
                        abs(float(best_bid_ask_amount2)))
                else:
                    amount_for_direction_instrument2 = number_multiple_10_and_round_0_digits(
                        abs(float(instrument_position2) - 0))
            else:
                amount_for_direction_instrument2 = 0

            if amount_for_direction_instrument1 <= amount_for_direction_instrument2 and \
                    amount_for_direction_instrument1 != 0:
                amount_for_direction = amount_for_direction_instrument1
            elif amount_for_direction_instrument2 < amount_for_direction_instrument1 and \
                    amount_for_direction_instrument2 != 0:
                amount_for_direction = amount_for_direction_instrument2
            else:
                amount_for_direction = 0

            if amount_for_direction >= 10 and summary_instrument1['size'] != 0 and \
                    instrument_buy_or_sell1 != summary_instrument1['direction'] and \
                    best_bid_ask_price1 != 0:
                if summary_instrument1['direction'] == 'buy':
                    connect.sell_limit(currency=str(summary_instrument1['instrument_name']),
                                       amount=amount_for_direction,
                                       price=float(best_bid_ask_price1))
                    list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                    list_monitor_log.append('Sell order'
                                            'instrument Name: ' + instrument_name_1 +
                                            'Amount order: ' + str(amount_for_direction) +
                                            'Price: ' + str(best_bid_ask_price1) +
                                            ' ')
                elif summary_instrument1['direction'] == 'sell':
                    connect.buy_limit(currency=str(summary_instrument1['instrument_name']),
                                      amount=amount_for_direction,
                                      price=float(best_bid_ask_price1))
                    list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                    list_monitor_log.append('Sell order'
                                            'instrument Name: ' + instrument_name_1 +
                                            'Amount order: ' + str(amount_for_direction) +
                                            'Price: ' + str(best_bid_ask_price1) +
                                            ' ')
                else:
                    pass
                time.sleep(5)
                connect.cancel_all()
            else:
                pass

            if amount_for_direction >= 10 and summary_instrument2['size'] != 0 and \
                    instrument_buy_or_sell2 != summary_instrument2['direction'] and \
                    best_bid_ask_price2 != 0:
                if summary_instrument2['direction'] == 'buy':
                    connect.sell_limit(currency=str(summary_instrument2['instrument_name']),
                                       amount=amount_for_direction,
                                       price=float(best_bid_ask_price2))
                    list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                    list_monitor_log.append('Sell order'
                                            'instrument Name: ' + instrument_name_2 +
                                            'Amount order: ' + str(amount_for_direction) +
                                            'Price: ' + str(best_bid_ask_price2) +
                                            ' ')
                elif summary_instrument2['direction'] == 'sell':
                    connect.buy_limit(currency=str(summary_instrument2['instrument_name']),
                                      amount=amount_for_direction,
                                      price=float(best_bid_ask_price2))
                    list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                    list_monitor_log.append('Sell order'
                                            'instrument Name: ' + instrument_name_2 +
                                            'Amount order: ' + str(amount_for_direction) +
                                            'Price: ' + str(best_bid_ask_price2) +
                                            ' ')
                else:
                    pass
                time.sleep(5)
                connect.cancel_all()
            else:
                pass

        elif positions_with_same_size_in_usd_or_currency == 'USD' and \
                (abs(float(total_amount / 2)) - abs(float(instrument_position1)) <= -10 or
                    abs(float(total_amount / 2)) - abs(float(instrument_position2)) <= -10 or
                    (abs(float(total_amount)) - (abs(float(instrument_position1)) +
                     abs(float(instrument_position2))) <= - 10)) and \
                ((instrument_buy_or_sell1 == summary_instrument1['direction'] and summary_instrument1['size'] != 0) and
                    (instrument_buy_or_sell2 == summary_instrument2['direction'] and summary_instrument2['size'] != 0)):
            
            if abs(float(total_amount / 2)) - abs(float(instrument_position1)) <= -10:
                if best_bid_ask_amount1 <= abs(abs(float(total_amount / 2)) - abs(float(instrument_position1))):
                    amount_for_max_postiion_instrument1 = number_multiple_10_and_round_0_digits(
                        best_bid_ask_amount1
                    )
                else:
                    amount_for_max_postiion_instrument1 = number_multiple_10_and_round_0_digits(
                        abs(abs(float(total_amount / 2)) - abs(float(instrument_position1)))
                    )
            else:
                amount_for_max_postiion_instrument1 = 0
                
            if abs(float(total_amount / 2)) - abs(float(instrument_position2)) <= -10:
                if best_bid_ask_amount2 <= abs(abs(float(total_amount / 2)) - abs(float(instrument_position2))):
                    amount_for_max_postiion_instrument2 = number_multiple_10_and_round_0_digits(
                        best_bid_ask_amount2
                    )
                else:
                    amount_for_max_postiion_instrument2 = number_multiple_10_and_round_0_digits(
                        abs(abs(float(total_amount / 2)) - abs(float(instrument_position2)))
                    )
            else:
                amount_for_max_postiion_instrument2 = 0
                
            if 0 != amount_for_max_postiion_instrument1 <= amount_for_max_postiion_instrument2:
                amount_for_max_postiion = amount_for_max_postiion_instrument1
            elif 0 != amount_for_max_postiion_instrument1 > amount_for_max_postiion_instrument2:
                amount_for_max_postiion = amount_for_max_postiion_instrument2
            else:
                amount_for_max_postiion = 0
            
            if amount_for_max_postiion >= 10 and abs(float(total_amount / 2)) - abs(float(instrument_position1)) <= -10:
                if summary_instrument1['direction'] == 'buy':
                    connect.sell_limit(currency=instrument_name_1,
                                       amount=float(amount_for_max_postiion),
                                       price=float(best_bid_ask_price1))
                    list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                    list_monitor_log.append(' Sell order'
                                            ' instrument Name: ' + instrument_name_1 +
                                            ' Amount order: ' + str(amount_for_max_postiion) +
                                            ' Price: ' + str(best_bid_ask_price1) +
                                            ' ')
                elif summary_instrument1['direction'] == 'sell':
                    connect.buy_limit(currency=instrument_name_1,
                                      amount=float(amount_for_max_postiion),
                                      price=float(best_bid_ask_price1))
                    list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                    list_monitor_log.append(' Buy order'
                                            ' instrument Name: ' + instrument_name_1 +
                                            ' Amount order: ' + str(amount_for_max_postiion) +
                                            ' Price: ' + str(best_bid_ask_price1) +
                                            ' ')
                else:
                    pass
            else:
                pass
            
            if amount_for_max_postiion >= 10 and abs(float(total_amount / 2)) - abs(float(instrument_position2)) <= -10:
                if summary_instrument2['direction'] == 'buy':
                    connect.sell_limit(currency=instrument_name_2,
                                       amount=float(amount_for_max_postiion),
                                       price=float(best_bid_ask_price2))
                    list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                    list_monitor_log.append(' Sell order'
                                            ' instrument Name: ' + instrument_name_2 +
                                            ' Amount order: ' + str(amount_for_max_postiion) +
                                            ' Price: ' + str(best_bid_ask_price2) +
                                            ' ')
                elif summary_instrument2['direction'] == 'sell':
                    connect.buy_limit(currency=instrument_name_2,
                                      amount=float(amount_for_max_postiion),
                                      price=float(best_bid_ask_price2))
                    list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                    list_monitor_log.append('Buy order'
                                            ' instrument Name: ' + instrument_name_2 +
                                            ' Amount order: ' + str(amount_for_max_postiion) +
                                            ' Price: ' + str(best_bid_ask_price2) +
                                            ' ')
                else:
                    pass
            else:
                pass
            time.sleep(5)
            connect.cancel_all()
            
        elif positions_with_same_size_in_usd_or_currency == 'USD' and \
            number_multiple_10_and_round_0_digits(abs(
                abs(instrument_position1) - abs(instrument_position2))) >= 10 and \
                there_are_bid_ask_offer is True and \
                number_multiple_10_and_round_0_digits(float(smaller_amount)) >= 10 and \
                ((instrument_buy_or_sell1 == summary_instrument1['direction'] and summary_instrument1['size'] != 0) or
                    (instrument_buy_or_sell2 == summary_instrument2['direction'] and summary_instrument2['size'] != 0)):
            
            instrument_amount_usd_for_check_postions = number_multiple_10_and_round_0_digits(
                float(smaller_amount))
            if abs(instrument_position1) > abs(instrument_position2) and summary_instrument1['direction'] == 'buy':
                connect.sell_limit(currency=instrument_name_1, 
                                   amount=instrument_amount_usd_for_check_postions,
                                   price=best_bid_ask_price1)
                list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                list_monitor_log.append('Sell order'
                                        'instrument Name: ' + instrument_name_1 +
                                        'Amount order: ' + str(instrument_amount_usd_for_check_postions) +
                                        'Price: ' + str(best_bid_ask_price1) +
                                        ' ')
                time.sleep(5)
                connect.cancel_all()
            elif abs(instrument_position1) > abs(instrument_position2) and summary_instrument1['direction'] == 'sell':
                connect.buy_limit(currency=instrument_name_1, 
                                  amount=instrument_amount_usd_for_check_postions, 
                                  price=best_bid_ask_price1)
                list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                list_monitor_log.append('Buy order'
                                        'instrument Name: ' + instrument_name_1 +
                                        'Amount order: ' + str(instrument_amount_usd_for_check_postions) +
                                        'Price: ' + str(best_bid_ask_price1)
                                        )
                time.sleep(5)
                connect.cancel_all()
            elif abs(instrument_position2) > abs(instrument_position1) and summary_instrument2['direction'] == 'buy':
                connect.sell_limit(currency=instrument_name_2, 
                                   amount=instrument_amount_usd_for_check_postions,
                                   price=best_bid_ask_price2)
                list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                list_monitor_log.append('Sell order'
                                        'instrument Name: ' + instrument_name_2 +
                                        'Amount order: ' + str(instrument_amount_usd_for_check_postions) +
                                        'Price: ' + str(best_bid_ask_price2) +
                                        ' ')
                time.sleep(5)
                connect.cancel_all()
            elif abs(instrument_position2) > abs(instrument_position1) and summary_instrument2['direction'] == 'sell':
                connect.buy_limit(currency=instrument_name_2, 
                                  amount=instrument_amount_usd_for_check_postions, 
                                  price=best_bid_ask_price2)
                list_monitor_log.append(' *** Instruments Checked - Orders Sent *** ')
                list_monitor_log.append('Buy order'
                                        'instrument Name: ' + instrument_name_2 +
                                        'Amount order: ' + str(instrument_amount_usd_for_check_postions) +
                                        'Price: ' + str(best_bid_ask_price2) +
                                        ' ')
                time.sleep(5)
                connect.cancel_all()
            else:
                list_monitor_log.append(' ***** ERROR in Check Instruments - Error Code: 1587 ***** ')
                connect.logwriter('\n***** ERROR in Check Instruments - Error Code: 1570 *****')
        else:
            list_monitor_log.append(' *** The instruments has NOT been checked *** ')

    def timestamp_till_expiration_instrument(instrument_name):
        from connection_arbitrage import connect
        currency = str
        if 'BTC' in instrument_name:
            currency = 'BTC'
        elif 'ETH' in instrument_name:
            currency = 'ETH'
        elif 'SOL' in instrument_name:
            currency = 'SOL'
        else:
            pass

        a5 = connect.get_instruments_future(currency=currency)

        dict_timestamp = {}
        for i in a5:
            dict_timestamp[i['instrument_name']] = i['expiration_timestamp']
        instrument_timestamp_till_expiration = dict_timestamp[str(instrument_name)]
        del dict_timestamp
        return int(instrument_timestamp_till_expiration)

    def annualized_premium(instrument_name):
        from connection_arbitrage import connect
        # % (mid future price / index price - 1) * 525600 / min till expiration

        if 'PERPETUAL' in str(instrument_name):
            return 0
        else:
            book_summary_instrument = connect.get_book_summary_by_instrument(instrument_name=instrument_name)
            # index_price
            index_price = float
            if 'BTC' in instrument_name:
                index_price = float(connect.index_price(currency='btc_usd')['index_price'])
                pass
            elif 'ETH' in instrument_name:
                index_price = float(connect.index_price(currency='eth_usd')['index_price'])
                pass
            elif 'SOL' in instrument_name:
                index_price = float(connect.index_price(currency='sol_usd')['index_price'])
            else:
                pass

            # no bid/ask offer
            if book_summary_instrument[0]['mid_price'] is None or book_summary_instrument[0]['mid_price'] == 'null':
                list_monitor_log.append('********** ' + str(instrument_name) +
                                        ' No bid/ask offer in annualized_premium **********')
                return 'No bid/ask offer'
            else:
                mid_price_future = float(book_summary_instrument[0]['mid_price'])
                timestamp_now = round(datetime.now().timestamp() * 1000)
                timestamp_expiration = timestamp_till_expiration_instrument(instrument_name=instrument_name)
                min_till_expiration = (timestamp_expiration - int(timestamp_now)) / 60000
                return round(float(((mid_price_future / index_price - 1) * 525600 / min_till_expiration) * 100), 2)

    def stop_gain(instrument_name_1, instrument_name_2,
                  summary_instrument1, summary_instrument2,
                  order_book_instrument1, order_book_instrument2,
                  set_exit_position_in_, set_exit_position_bigger_lower_, set_exit_position_value_):
        from lists import list_monitor_log
        from connection_arbitrage import connect

        list_monitor_log.append(' *** Stop Gain Check *** ')
        list_monitor_log.append(' Stop Gains selected in: ' +
                                str(set_exit_position_in_) +
                                ' ' +
                                str(set_exit_position_bigger_lower_) +
                                ' ' +
                                str(set_exit_position_value_) +
                                ' '
                                )
        # Args
        average_price_position_instrument1 = float(summary_instrument1['average_price'])
        average_price_position_instrument2 = float(summary_instrument2['average_price'])

        instrument_position1 = float(summary_instrument1['size'])
        instrument_position2 = float(summary_instrument2['size'])

        instrument_position_currency1 = float(summary_instrument1['size_currency'])
        instrument_position_currency2 = float(summary_instrument2['size_currency'])

        if summary_instrument1['direction'] == 'buy':
            profit_loss_in_usd_instrument1 = \
                (float(order_book_instrument1['best_bid_price']) - float(average_price_position_instrument1)) * \
                abs(instrument_position_currency1)
            instrument_price1 = float(order_book_instrument1['best_bid_price'])
        elif summary_instrument1['direction'] == 'sell':
            profit_loss_in_usd_instrument1 = \
                (float(average_price_position_instrument1) - float(order_book_instrument1['best_ask_price'])) * \
                abs(instrument_position_currency1)
            instrument_price1 = float(order_book_instrument1['best_ask_price'])
        else:
            profit_loss_in_usd_instrument1 = 0
            instrument_price1 = 0

        if summary_instrument2['direction'] == 'buy':
            profit_loss_in_usd_instrument2 = \
                (float(order_book_instrument2['best_bid_price']) - float(average_price_position_instrument2)) * \
                abs(instrument_position_currency2)
            instrument_price2 = float(order_book_instrument2['best_bid_price'])
        elif summary_instrument2['direction'] == 'sell':
            profit_loss_in_usd_instrument2 = \
                (float(average_price_position_instrument2) - float(order_book_instrument2['best_ask_price'])) * \
                abs(instrument_position_currency2)
            instrument_price2 = float(order_book_instrument2['best_ask_price'])
        else:
            profit_loss_in_usd_instrument2 = 0
            instrument_price2 = 0

        profit_loss_in_usd_total = float(profit_loss_in_usd_instrument1) + \
            float(profit_loss_in_usd_instrument2)

        # strategy exit position in Profit_
        if set_exit_position_in_ == 'Profit_%':
            profit_loss_percentage = profit_loss_in_usd_total * 100 / (
                    abs(instrument_position1) + abs(instrument_position2))
            if set_exit_position_bigger_lower_ == '>':
                if float(profit_loss_percentage) > float(set_exit_position_value_):
                    list_monitor_log.append(' *** Stopped position gain *** ')
                    list_monitor_log.append(str(set_exit_position_in_) + ': ' + str(profit_loss_percentage) + '%. ')
                    return True
                else:
                    list_monitor_log.append(' *** Stop Gain checked *** ')
                    list_monitor_log.append(str(set_exit_position_in_) + ': ' + str(profit_loss_percentage) + '%. ')
                    return False
            elif set_exit_position_bigger_lower_ == '<':
                if float(profit_loss_percentage) < float(set_exit_position_value_):
                    list_monitor_log.append(' *** Stopped position gain *** ')
                    list_monitor_log.append(str(set_exit_position_in_) + ': ' + str(profit_loss_percentage) + '%. ')
                    return True
                else:
                    list_monitor_log.append(' *** Stop Gain checked *** ')
                    list_monitor_log.append(str(set_exit_position_in_) + ': ' + str(profit_loss_percentage) + '%. ')
                    return False
            else:
                list_monitor_log.append(' ***** ERROR in Stop Gain check - Error Code 1509 *** ')
                list_monitor_log.append(str(set_exit_position_in_) + ': ' + str(profit_loss_percentage) + '%. ')
                connect.logwriter('\n***** ERROR in Stop Gain check - Error Code 1511 *** ')
                connect.logwriter('\n' + str(set_exit_position_in_) + ': ' + str(profit_loss_percentage) + '%. ')
                return False

        # strategy exit position in Difference_%
        elif set_exit_position_in_ == 'Difference_%':
            difference_instrument2_instrument1_percentage = (
                abs(instrument_price2) - abs(instrument_price1)) * 100 / abs(instrument_price1)
            if set_exit_position_bigger_lower_ == '>':
                if difference_instrument2_instrument1_percentage > \
                        float(set_exit_position_value_):
                    list_monitor_log.append(' *** Stopped position gain *** ')
                    list_monitor_log.append(
                        str(set_exit_position_in_) + ': ' + str(difference_instrument2_instrument1_percentage) + '%. ')
                    return True
                else:
                    list_monitor_log.append(' *** Stop Gain checked *** ')
                    list_monitor_log.append(
                        str(set_exit_position_in_) + ': ' + str(difference_instrument2_instrument1_percentage) + '%. ')
                    return False
            elif set_exit_position_bigger_lower_ == '<':
                if difference_instrument2_instrument1_percentage < \
                        float(set_exit_position_value_):
                    list_monitor_log.append(' *** Stopped position gain *** ')
                    list_monitor_log.append(
                        str(set_exit_position_in_) + ': ' + str(difference_instrument2_instrument1_percentage) + '%. ')
                    return True
                else:
                    list_monitor_log.append(' *** Stop Gain checked *** ')
                    list_monitor_log.append(
                        str(set_exit_position_in_) + ': ' + str(difference_instrument2_instrument1_percentage) + '%. ')
                    return False
            else:
                list_monitor_log.append(' ***** ERROR in Stop Gain check - Error Code 1544 *** ')
                list_monitor_log.append(
                    str(set_exit_position_in_) + ': ' + str(difference_instrument2_instrument1_percentage) + '%. ')
                connect.logwriter('\n***** ERROR in Stop Gain check - Error Code 1547 *** ')
                connect.logwriter(
                    '\n' + str(set_exit_position_in_) + ': ' + str(
                        difference_instrument2_instrument1_percentage) + '%. ')
                return False

        # strategy exit position in Difference_USD
        elif set_exit_position_in_ == 'Difference_USD':
            instrument2_intrument1_difference_in_usd = abs(instrument_price2) - abs(instrument_price1)
            if set_exit_position_bigger_lower_ == '>':
                if instrument2_intrument1_difference_in_usd > float(set_exit_position_value_):
                    list_monitor_log.append(' *** Stopped position gain *** ')
                    list_monitor_log.append(
                        str(set_exit_position_in_) + ': ' + str(instrument2_intrument1_difference_in_usd) + ' USD. ')
                    return True
                else:
                    list_monitor_log.append(' *** Stop Gain checked *** ')
                    list_monitor_log.append(
                        str(set_exit_position_in_) + ': ' + str(instrument2_intrument1_difference_in_usd) + ' USD. ')
                    return False
            elif set_exit_position_bigger_lower_ == '<':
                if instrument2_intrument1_difference_in_usd < float(set_exit_position_value_):
                    list_monitor_log.append(' *** Stopped position gain *** ')
                    list_monitor_log.append(
                        str(set_exit_position_in_) + ': ' + str(instrument2_intrument1_difference_in_usd) + ' USD. ')
                    return True
                else:
                    list_monitor_log.append(' *** Stop Gain checked *** ')
                    list_monitor_log.append(
                        str(set_exit_position_in_) + ': ' + str(instrument2_intrument1_difference_in_usd) + ' USD. ')
                    return False
            else:
                list_monitor_log.append('***** ERROR in Stop Gain check - Error Code 1579 ***')
                list_monitor_log.append(
                    str(set_exit_position_in_) + ': ' + str(instrument2_intrument1_difference_in_usd) + ' USD. ')
                connect.logwriter('***** ERROR in Stop Gain check - Error Code 1582 ***')
                connect.logwriter(
                    str(set_exit_position_in_) + ': ' + str(instrument2_intrument1_difference_in_usd) + ' USD. ')
                return False

        # strategy exit position in Difference_Premium
        elif set_exit_position_in_ == 'Difference_Premium':
            annualized_premium1 = annualized_premium(instrument_name=instrument_name_1)
            annualized_premium2 = annualized_premium(instrument_name=instrument_name_2)
            if annualized_premium1 == 'No bid/ask offer' or annualized_premium2 == 'No bid/ask offer':
                list_monitor_log.append(' ***** Stop Gain NO checked - No bid/ask offer ***** ')
                connect.logwriter(' ***** Stop Gain NO checked - No bid/ask offer ***** ')
                return False
            else:
                instrument2_instrument1_annualized_premium = float(annualized_premium2) - float(annualized_premium1)
                if set_exit_position_bigger_lower_ == '>':
                    if instrument2_instrument1_annualized_premium > float(set_exit_position_value_):
                        list_monitor_log.append(' *** Stopped position gain: ' + str(instrument_name_2) +
                                                ' > ' + str(set_exit_position_value_) + 'AP Difference ' +
                                                str(instrument_name_1) + '. ' +
                                                str(instrument2_instrument1_annualized_premium) + ' *** ')
                        return True
                    else:
                        list_monitor_log.append(' *** Stop Gain checked *** ')
                        list_monitor_log.append(
                            str(set_exit_position_in_) + ': ' + str(instrument2_instrument1_annualized_premium))
                        list_monitor_log.append(
                            str(instrument_name_1) + ' Annualized Premium: ' + str(annualized_premium1) + ' %. ')
                        list_monitor_log.append(
                            str(instrument_name_2) + ' Annualized Premium: ' + str(annualized_premium2) + ' %. ')
                        return False
                elif set_exit_position_bigger_lower_ == '<':
                    if instrument2_instrument1_annualized_premium < float(set_exit_position_value_):
                        list_monitor_log.append(' *** Stopped position gain: ' + str(instrument_name_2) +
                                                ' < ' + str(set_exit_position_value_) + 'AP Difference ' +
                                                str(instrument_name_1) + '. ' +
                                                str(instrument2_instrument1_annualized_premium) + ' *** ')
                        return True
                    else:
                        list_monitor_log.append(' *** Stop Gain checked *** ')
                        list_monitor_log.append(
                            str(set_exit_position_in_) + ': ' + str(instrument2_instrument1_annualized_premium))
                        list_monitor_log.append(
                            str(instrument_name_1) + ' Annualized Premium: ' + str(annualized_premium1) + ' %')
                        list_monitor_log.append(
                            str(instrument_name_2) + ' Annualized Premium: ' + str(annualized_premium2) + ' %. ')
                        return False
                else:
                    list_monitor_log.append(' ***** ERROR in Stop Gain check - Error Code 1825 *** ')
                    list_monitor_log.append(
                        str(set_exit_position_in_) + ': ' + str(instrument2_instrument1_annualized_premium))
                    connect.logwriter('\n***** ERROR in Stop Gain check - Error Code 1828 ***')
                    connect.logwriter(
                        '\n' + str(set_exit_position_in_) + ': ' + str(instrument2_instrument1_annualized_premium))
                    return False
        else:
            list_monitor_log.append('***** ERROR in Stop Gain check - Error Code 1833 ***** ' + str(
                set_exit_position_in_) + ' ' + str(set_exit_position_value_) + ' *** ')
            connect.logwriter('\n***** ERROR in Stop Gain check - Error Code 1835 ***** ' + str(
                set_exit_position_in_) + ' ' + str(set_exit_position_value_))
            return False

    def stop_loss(set_stop_loss_in_, set_stop_loss_value_,
                  order_book_instrument1, order_book_instrument2,
                  summary_instrument1, summary_instrument2):
        from connection_arbitrage import connect
        from lists import list_monitor_log

        list_monitor_log.append(' *** Stop Loss Check *** ')
        list_monitor_log.append('Stop Loss selected in: ' +
                                str(set_stop_loss_in_) +
                                ' ' +
                                str(set_stop_loss_value_) +
                                ' ')
        # Args

        average_price_position_instrument1 = float(summary_instrument1['average_price'])
        average_price_position_instrument2 = float(summary_instrument2['average_price'])

        instrument_position1 = float(summary_instrument1['size'])
        instrument_position2 = float(summary_instrument2['size'])

        instrument_position1_currency = float(summary_instrument1['size_currency'])
        instrument_position2_currency = float(summary_instrument2['size_currency'])

        instrument_buy_or_sell1 = summary_instrument1['direction']
        instrument_buy_or_sell2 = summary_instrument2['direction']

        if instrument_buy_or_sell1 == 'buy' and order_book_instrument1['best_bid_amount'] != 0:
            best_bid_ask_price_in_usd_instrument1 = float(order_book_instrument1['best_bid_price'])
        elif instrument_buy_or_sell1 == 'sell' and order_book_instrument1['best_ask_amount'] != 0:
            best_bid_ask_price_in_usd_instrument1 = float(order_book_instrument1['best_ask_price'])
        else:
            best_bid_ask_price_in_usd_instrument1 = 0

        if instrument_buy_or_sell2 == 'buy' and order_book_instrument1['best_bid_amount'] != 0:
            best_bid_ask_price_in_usd_instrument2 = float(order_book_instrument2['best_bid_price'])
        elif instrument_buy_or_sell2 == 'sell' and order_book_instrument1['best_ask_amount'] != 0:
            best_bid_ask_price_in_usd_instrument2 = float(order_book_instrument2['best_ask_price'])
        else:
            best_bid_ask_price_in_usd_instrument2 = 0

        if summary_instrument1['direction'] == 'buy':
            profit_loss_in_usd_instrument1 = \
                (float(best_bid_ask_price_in_usd_instrument1) - float(average_price_position_instrument1)) * \
                abs(instrument_position1_currency)
            if best_bid_ask_price_in_usd_instrument1 != 0:
                profit_loss_in_currency_instrument1 = \
                    profit_loss_in_usd_instrument1 / best_bid_ask_price_in_usd_instrument1
            else:
                profit_loss_in_currency_instrument1 = 0
        elif summary_instrument1['direction'] == 'sell':
            profit_loss_in_usd_instrument1 = \
                (float(average_price_position_instrument1) - float(best_bid_ask_price_in_usd_instrument1)) * \
                abs(instrument_position1_currency)
            if best_bid_ask_price_in_usd_instrument1 != 0:
                profit_loss_in_currency_instrument1 = \
                    profit_loss_in_usd_instrument1 / best_bid_ask_price_in_usd_instrument1
            else:
                profit_loss_in_currency_instrument1 = 0
        else:
            profit_loss_in_usd_instrument1 = 0
            profit_loss_in_currency_instrument1 = 0

        if summary_instrument2['direction'] == 'buy':
            profit_loss_in_usd_instrument2 = \
                (float(best_bid_ask_price_in_usd_instrument2) - float(average_price_position_instrument2)) * \
                abs(instrument_position2_currency)
            if best_bid_ask_price_in_usd_instrument2 != 0:
                profit_loss_in_currency_instrument2 = \
                    profit_loss_in_usd_instrument2 / best_bid_ask_price_in_usd_instrument2
            else:
                profit_loss_in_currency_instrument2 = 0
        elif summary_instrument2['direction'] == 'sell':
            profit_loss_in_usd_instrument2 = \
                (float(average_price_position_instrument2) - float(best_bid_ask_price_in_usd_instrument2)) * \
                abs(instrument_position2_currency)
            if best_bid_ask_price_in_usd_instrument2 != 0:
                profit_loss_in_currency_instrument2 = \
                    profit_loss_in_usd_instrument2 / best_bid_ask_price_in_usd_instrument2
            else:
                profit_loss_in_currency_instrument2 = 0
        else:
            profit_loss_in_usd_instrument2 = 0
            profit_loss_in_currency_instrument2 = 0

        profit_loss_in_usd_total = float(profit_loss_in_usd_instrument1) + float(profit_loss_in_usd_instrument2)
        instrument_total_profit_loss_in_currency = float(
            profit_loss_in_currency_instrument1) + float(profit_loss_in_currency_instrument2)

        instrument_price1 = float(best_bid_ask_price_in_usd_instrument1)
        instrument_price2 = float(best_bid_ask_price_in_usd_instrument2)

        # Args - the end

        if instrument_price1 == 0 or instrument_price2 == 0:
            list_monitor_log.append(' *** No Bid/Ask Offer into Stop Loss Check *** ')
            list_monitor_log.append('instrument_price1: ' +
                                    str(instrument_price1) +
                                    'instrument_price2: ' +
                                    str(instrument_price2) + ' ')
            list_monitor_log.append(' ***** Stop Loss has NOT been Checked ***** ')
            return False

        elif set_stop_loss_in_ == 'USD:':
            if profit_loss_in_usd_total < float(set_stop_loss_value_):
                connect.logwriter('\n***** Stop Loss has been executed ***** ')
                list_monitor_log.append(' ***** Stop Loss has been executed ***** ')
                list_monitor_log.append(' set_stop_loss_in_: ' + str(set_stop_loss_in_) + '. ' +
                                        ' set_stop_loss_value_: ' + str(set_stop_loss_value_) + '. ' +
                                        ' profit_loss_in_usd_total: ' + str(profit_loss_in_usd_total) + '. ')
                return True
            else:
                list_monitor_log.append(' *** Stop Loss Checked *** ')
                list_monitor_log.append(' set_stop_loss_in_: ' + str(set_stop_loss_in_) + '. ' +
                                        ' set_stop_loss_value_: ' + str(set_stop_loss_value_) + '. ' +
                                        ' profit_loss_in_usd_total: ' + str(profit_loss_in_usd_total) + '. ')
                return False

        elif set_stop_loss_in_ == 'BTC/ETH:':
            if instrument_total_profit_loss_in_currency < float(set_stop_loss_value_):
                connect.logwriter('\n***** Stop Loss has been executed ***** ')
                list_monitor_log.append(' ***** Stop Loss has been executed ***** ')
                list_monitor_log.append(' set_stop_loss_in_: ' + str(set_stop_loss_in_) + '. ' +
                                        ' set_stop_loss_value_: ' + str(set_stop_loss_value_) + '. ' +
                                        ' instrument_total_profit_loss_in_currency: ' +
                                        str(instrument_total_profit_loss_in_currency) + '. ')
                return True
            else:
                list_monitor_log.append(' *** Stop Loss Checked *** ')
                list_monitor_log.append(' set_stop_loss_in_: ' + str(set_stop_loss_in_) + '. ' +
                                        ' set_stop_loss_value_: ' + str(set_stop_loss_value_) + '. ' +
                                        ' instrument_total_profit_loss_in_currency: ' +
                                        str(instrument_total_profit_loss_in_currency) + '. ')
                return False

        elif set_stop_loss_in_ == '%:':
            percentage_stop_loss = profit_loss_in_usd_total * 100 / (abs(
                instrument_position1) + abs(instrument_position2))

            if percentage_stop_loss < float(set_stop_loss_value_):
                connect.logwriter('***** Stop Loss has been executed *****')
                list_monitor_log.append('***** Stop Loss has been executed *****')
                return True
            else:
                list_monitor_log.append('*** Stop Loss Checked ***')
                list_monitor_log.append(' set_stop_loss_in_: ' + str(set_stop_loss_in_) + '. ' +
                                        ' set_stop_loss_value_: ' + str(set_stop_loss_value_) + '. ' +
                                        ' percentage_stop_loss: ' +
                                        str(percentage_stop_loss) + '. ')
                return False
        else:
            connect.logwriter('\n ********** ERROR - Stop Loss has NOT been Checked - Error Code 1794 **********')
            list_monitor_log.append('********** ERROR - Stop Loss has NOT been Checked - Error Code 1795 **********')
            connect.logwriter('\nset_stop_loss_in_: ' + str(set_stop_loss_in_) + '. ' +
                              '\nset_stop_loss_value_: ' + str(set_stop_loss_value_) + '. ')
            return False

    def strategy_entry(instrument_name_1, instrument_name_2,
                       best_bid_ask_price_in_usd_instrument1, best_bid_ask_price_in_usd_instrument2,
                       set_entry_position_in_, set_entry_position_bigger_lower_, set_entry_position_value_):
        from lists import list_monitor_log
        from connection_arbitrage import connect

        list_monitor_log.append(' *** Trade Opening Setup Check *** ')
        list_monitor_log.append(' Trade setup: ' +
                                str(set_entry_position_in_) +
                                ' ' +
                                str(set_entry_position_bigger_lower_) +
                                ' ' +
                                str(set_entry_position_value_) + ' '
                                )
        # Args

        instrument_price1 = float(best_bid_ask_price_in_usd_instrument1)
        instrument_price2 = float(best_bid_ask_price_in_usd_instrument2)

        # Entry position in %
        if set_entry_position_in_ == '%':
            difference_instrument2_instrument1_percentage = (
                abs(instrument_price2) - abs(instrument_price1)) * 100 / abs(instrument_price1)
            if set_entry_position_bigger_lower_ == '>':
                if difference_instrument2_instrument1_percentage > float(set_entry_position_value_):
                    list_monitor_log.append(' *** Opened position:' + str(instrument_name_2) +
                                            ' > ' + str(set_entry_position_value_) + '% ' +
                                            str(instrument_name_1) + '. ' +
                                            str(difference_instrument2_instrument1_percentage) + '%. ')
                    return True
                else:
                    list_monitor_log.append(' *** Trade Opening Setup Checked *** ')
                    list_monitor_log.append(
                        str(instrument_name_1) + ' ' + str(difference_instrument2_instrument1_percentage) +
                        'difference of the ' +
                        str(instrument_name_2) + ' ')
                    return False
            elif set_entry_position_bigger_lower_ == '<':
                if difference_instrument2_instrument1_percentage < float(set_entry_position_value_):
                    list_monitor_log.append(' *** Opened position:' + str(instrument_name_2) +
                                            ' < ' + str(set_entry_position_value_) + '% ' +
                                            str(instrument_name_1) + '. ' +
                                            str(difference_instrument2_instrument1_percentage) + '%. ')
                    return True
                else:
                    list_monitor_log.append(' *** Trade Opening Setup Checked *** ')
                    list_monitor_log.append(
                        str(instrument_name_2) + ' ' + str(difference_instrument2_instrument1_percentage) +
                        '% difference of the ' +
                        str(instrument_name_1) + ' ')
                    return False
            else:
                list_monitor_log.append(' ***** ERROR in Trade Opening Setup Check - Error Code 1852 ***** ')
                list_monitor_log.append('set_entry_position_in_' +
                                        str(set_entry_position_in_) + ': ' +
                                        str(difference_instrument2_instrument1_percentage) + '%. ')
                connect.logwriter('\n***** ERROR in Trade Opening Setup Check - Error Code 1856 *****')
                connect.logwriter('\nset_entry_position_in_: ' +
                                  str(set_entry_position_in_) + ': ' +
                                  str(difference_instrument2_instrument1_percentage) + '%. ')
                return False

        # Entry position in USD
        elif set_entry_position_in_ == 'USD':
            instrument2_intrument1_difference_in_usd = abs(instrument_price2) - abs(instrument_price1)
            if set_entry_position_bigger_lower_ == '>':
                if instrument2_intrument1_difference_in_usd > set_entry_position_value_:
                    list_monitor_log.append(' *** Opened position:' + str(instrument_name_2) +
                                            ' > ' + str(set_entry_position_value_) + 'USD ' +
                                            str(instrument_name_1) + '. ' +
                                            str(instrument2_intrument1_difference_in_usd) + 'USD ')
                    return True
                else:
                    list_monitor_log.append(' *** Trade Opening Setup Checked *** ')
                    list_monitor_log.append(
                        str(instrument_name_2) + ' ' + str(instrument2_intrument1_difference_in_usd) +
                        'USD difference of the ' +
                        str(instrument_name_1) + ' ')
                    return False
            elif set_entry_position_bigger_lower_ == '<':
                if instrument2_intrument1_difference_in_usd < set_entry_position_value_:
                    list_monitor_log.append(' *** Opened position:' + str(instrument_name_2) +
                                            ' > ' + str(set_entry_position_value_) + 'USD ' +
                                            str(instrument_name_1) + '. ' +
                                            str(instrument2_intrument1_difference_in_usd) + 'USD ')
                    return True
                else:
                    list_monitor_log.append(' *** Trade Opening Setup Checked *** ')
                    list_monitor_log.append(
                        str(instrument_name_2) + ' ' + str(instrument2_intrument1_difference_in_usd) +
                        'USD difference of the ' +
                        str(instrument_name_1) + ' ')
                    return False
            else:
                list_monitor_log.append(' ***** ERROR in Trade Opening Setup Check - Error Code 1894 ***** ')
                list_monitor_log.append(' set_entry_position_in_' +
                                        str(set_entry_position_in_) + ': ' +
                                        str(instrument2_intrument1_difference_in_usd) + 'USD ')
                connect.logwriter('\n***** ERROR in Trade Opening Setup Check - Error Code 1898 *****')
                connect.logwriter('\nset_entry_position_in_' +
                                  str(set_entry_position_in_) + ': ' +
                                  str(instrument2_intrument1_difference_in_usd) + 'USD ')
                return False

        # Entry position in Premium(Annualized)
        elif set_entry_position_in_ == 'Premium(Annualized)':
            annualized_premium1 = annualized_premium(instrument_name=instrument_name_1)
            annualized_premium2 = annualized_premium(instrument_name=instrument_name_2)
            if annualized_premium1 == 'No bid/ask offer' or annualized_premium2 == 'No bid/ask offer':
                list_monitor_log.append(' ***** Trade Opening Setup NO Checked - No bid/ask offer ***** ')
                return False
            else:
                instrument2_instrument1_annualized_premium = float(annualized_premium2) - float(annualized_premium1)
                if set_entry_position_bigger_lower_ == '>':
                    if instrument2_instrument1_annualized_premium > float(set_entry_position_value_):
                        list_monitor_log.append(' *** Opened position:' + str(instrument_name_2) +
                                                ' > ' + str(set_entry_position_value_) + 'AP Difference ' +
                                                str(instrument_name_1) + '. ' +
                                                str(instrument2_instrument1_annualized_premium) + ' ')
                        return True
                    else:
                        list_monitor_log.append(' *** Trade Opening Setup Checked *** ')
                        list_monitor_log.append(
                            str(set_entry_position_in_) + ': ' + str(instrument2_instrument1_annualized_premium))
                        list_monitor_log.append(
                            str(instrument_name_1) + ' Annualized Premium: ' + str(annualized_premium1) + ' %')
                        list_monitor_log.append(
                            str(instrument_name_2) + ' Annualized Premium: ' + str(annualized_premium2) + ' %. ')
                        return False
                elif set_entry_position_bigger_lower_ == '<':
                    if instrument2_instrument1_annualized_premium > float(set_entry_position_value_):
                        list_monitor_log.append(' *** Opened position:' + str(instrument_name_2) +
                                                ' < ' + str(set_entry_position_value_) + 'AP Difference ' +
                                                str(instrument_name_1) + '. ' +
                                                str(instrument2_instrument1_annualized_premium) + ' ')
                        return True
                    else:
                        list_monitor_log.append(' *** Trade Opening Setup Checked *** ')
                        list_monitor_log.append(
                            str(set_entry_position_in_) + ': ' + str(instrument2_instrument1_annualized_premium))
                        list_monitor_log.append(
                            str(instrument_name_1) + ' Annualized Premium: ' + str(annualized_premium1) + ' %')
                        list_monitor_log.append(
                            str(instrument_name_2) + ' Annualized Premium: ' + str(annualized_premium2) + ' %. ')
                        return False
                else:
                    list_monitor_log.append(' ***** ERROR in Stop Gain check - Error Code 2141 *** ')
                    list_monitor_log.append(
                        str(set_entry_position_in_) + ': ' + str(instrument2_instrument1_annualized_premium))
                    connect.logwriter('\n***** ERROR in Stop Gain check - Error Code 2144 ***')
                    connect.logwriter(
                        '\n' + str(set_entry_position_in_) + ': ' + str(instrument2_instrument1_annualized_premium))
                    return False
        else:
            list_monitor_log.append(' ***** ERROR in Stop Gain check - Error Code 2149 ***** ' + str(
                set_entry_position_in_) + ' ' + str(set_entry_position_value_) + ' ')
            connect.logwriter('\n***** ERROR in Stop Gain check - Error Code 2151 ***** ' + str(
                set_entry_position_in_) + ' ' + str(set_entry_position_value_))
            return False

    def arbitrage_strategy():
        global index_greeks_print_on_off
        global strategy_on_off
        global what_instrument
        from lists import list_monitor_log

        sinal.ui_signal1.emit({
            'object_signal': 'setup_arbitrage_strategy_started',
            'msg': ''
        })

        strategy_on_off = 'on'

        # Args statics
        instrument_name_1 = str(
            ConfigAndInstrumentsSaved().instrument_name_construction_from_file(instrument_number=1)
        )
        instrument_buy_or_sell1 = str(
            ConfigAndInstrumentsSaved().instrument_buy_or_sell(instrument_number=1)
        )

        instrument_name_2 = str(
            ConfigAndInstrumentsSaved().instrument_name_construction_from_file(instrument_number=2)
        )
        instrument_buy_or_sell2 = str(
            ConfigAndInstrumentsSaved().instrument_buy_or_sell(instrument_number=2)
        )

        total_amount = float(
            ConfigAndInstrumentsSaved().total_amount_saved()
        )

        instrument_amount1_usd_before_trade = int(
            number_multiple_10_and_round_0_digits(number=total_amount / 2)
        )
        instrument_amount2_usd_before_trade = instrument_amount1_usd_before_trade

        positions_with_same_size_in_usd_or_currency = ConfigAndInstrumentsSaved().positions_with_same_size_in()

        set_entry_position_in_ = ConfigAndInstrumentsSaved().set_entry_position_in()
        set_entry_position_bigger_lower_ = ConfigAndInstrumentsSaved().set_entry_position_bigger_lower()
        set_entry_position_value_ = float(ConfigAndInstrumentsSaved().set_entry_position_value())

        set_exit_position_in_ = ConfigAndInstrumentsSaved().set_exit_position_in()
        set_exit_position_bigger_lower_ = ConfigAndInstrumentsSaved().set_exit_position_bigger_lower()
        set_exit_position_value_ = ConfigAndInstrumentsSaved().set_exit_position_value()

        set_stop_loss_in_ = str(ConfigAndInstrumentsSaved().set_stop_loss_in())
        set_stop_loss_value_ = float(ConfigAndInstrumentsSaved().set_stop_loss_value())

        stop_loss_counter = 0

        check_instruments_positions_true_or_false = False

        # Strategy arbitrage
        list_monitor_log.append('***** Arbitrage Started *****')
        while strategy_on_off == 'on':
            from lists import list_monitor_log
            try:
                from connection_arbitrage import connect

                # Args modifically

                summary_instrument1 = connect.get_position(instrument_name=instrument_name_1)
                summary_instrument2 = connect.get_position(instrument_name=instrument_name_2)

                instrument_position1 = float(summary_instrument1['size'])
                instrument_position2 = float(summary_instrument2['size'])

                order_book_instrument1 = connect.get_order_book(instrument_name=instrument_name_1)
                order_book_instrument2 = connect.get_order_book(instrument_name=instrument_name_2)

                # Args modifically - smaller_amount_dic (entry) and best_bid_ask_price1 and best_bid_ask_price2 - start

                smaller_amount_dic = dict()
                smaller_amount_dic.clear()
                # qto falta negociar
                smaller_amount_dic[
                    'abs(instrument_amount1_usd_before_trade) - abs(instrument_position1)'] = \
                    number_multiple_10_and_round_0_digits(
                        abs(instrument_amount1_usd_before_trade) - abs(instrument_position1)
                    )
                smaller_amount_dic[
                    'abs(instrument_amount2_usd_before_trade) - abs(instrument_position2)'] = \
                    number_multiple_10_and_round_0_digits(
                        abs(instrument_amount2_usd_before_trade) - abs(instrument_position2)
                    )

                if instrument_buy_or_sell1 == 'buy' and order_book_instrument1['best_ask_amount'] != 0:
                    best_bid_ask_amount1 = float(order_book_instrument1['best_ask_amount'])
                    best_bid_ask_price1 = float(order_book_instrument1['best_ask_price'])
                elif instrument_buy_or_sell1 == 'sell' and order_book_instrument1['best_bid_amount'] != 0:
                    best_bid_ask_amount1 = float(order_book_instrument1['best_bid_amount'])
                    best_bid_ask_price1 = float(order_book_instrument1['best_bid_price'])
                else:
                    best_bid_ask_amount1 = 0
                    best_bid_ask_price1 = 0

                if instrument_buy_or_sell2 == 'buy' and order_book_instrument2['best_ask_amount'] != 0:
                    best_bid_ask_amount2 = float(order_book_instrument2['best_ask_amount'])
                    best_bid_ask_price2 = float(order_book_instrument2['best_ask_price'])
                elif instrument_buy_or_sell2 == 'sell' and order_book_instrument2['best_bid_amount'] != 0:
                    best_bid_ask_amount2 = float(order_book_instrument2['best_bid_amount'])
                    best_bid_ask_price2 = float(order_book_instrument2['best_bid_price'])
                else:
                    best_bid_ask_amount2 = 0
                    best_bid_ask_price2 = 0

                smaller_amount_dic['best_bid_ask_amount1'] = number_multiple_10_and_round_0_digits(
                    abs(float(best_bid_ask_amount1))
                )
                smaller_amount_dic['best_bid_ask_amount2'] = number_multiple_10_and_round_0_digits(
                    abs(float(best_bid_ask_amount2))
                )                

                if len(smaller_amount_dic) > 0:
                    smaller_amount_name = min(smaller_amount_dic, key=smaller_amount_dic.get)  # name
                    smaller_amount = smaller_amount_dic.get(smaller_amount_name, 0)  # Valor
                else:
                    smaller_amount = 0  # valor
                    pass
                # Args modifically - smaller_amount_dic (entry) and best_bid_ask_price1 and best_bid_ask_price2 /the end

                # Args modifically - smaller_amount_dic_for_stop_gain - start ******************************************
                smaller_amount_for_stop_gain_dic = dict()
                smaller_amount_for_stop_gain_dic.clear()
                # position current
                smaller_amount_for_stop_gain_dic['abs(instrument_position1)'] = number_multiple_10_and_round_0_digits(
                    abs(instrument_position1))
                smaller_amount_for_stop_gain_dic['abs(instrument_position2)'] = number_multiple_10_and_round_0_digits(
                        abs(instrument_position2))

                if instrument_buy_or_sell1 == 'buy' and order_book_instrument1['best_bid_amount'] != 0:
                    best_bid_ask_amount_for_stop_gain_dict1 = float(order_book_instrument1['best_bid_amount'])
                    smaller_amount_for_stop_gain_dic[
                        'best_bid_ask_amount_for_stop_gain_dict1'] = number_multiple_10_and_round_0_digits(
                        abs(float(best_bid_ask_amount_for_stop_gain_dict1)))
                    best_bid_ask_price_for_stop_gain_dict1 = float(order_book_instrument1['best_bid_price'])
                elif instrument_buy_or_sell1 == 'sell' and order_book_instrument1['best_ask_amount'] != 0:
                    best_bid_ask_amount_for_stop_gain_dict1 = float(order_book_instrument1['best_ask_amount'])
                    smaller_amount_for_stop_gain_dic[
                        'best_bid_ask_amount_for_stop_gain_dict1'] = number_multiple_10_and_round_0_digits(
                        abs(float(best_bid_ask_amount_for_stop_gain_dict1)))
                    best_bid_ask_price_for_stop_gain_dict1 = float(order_book_instrument1['best_ask_price'])
                else:
                    best_bid_ask_amount_for_stop_gain_dict1 = 0
                    smaller_amount_for_stop_gain_dic[
                        'best_bid_ask_amount_for_stop_gain_dict1'] = number_multiple_10_and_round_0_digits(
                        abs(float(best_bid_ask_amount_for_stop_gain_dict1)))
                    best_bid_ask_price_for_stop_gain_dict1 = 0

                if instrument_buy_or_sell2 == 'buy' and order_book_instrument2['best_bid_amount'] != 0:
                    best_bid_ask_amount_for_stop_gain_dict2 = float(order_book_instrument2['best_bid_amount'])
                    smaller_amount_for_stop_gain_dic[
                        'best_bid_ask_amount_for_stop_gain_dict2'] = number_multiple_10_and_round_0_digits(
                        abs(float(best_bid_ask_amount_for_stop_gain_dict2)))
                    best_bid_ask_price_for_stop_gain_dict2 = float(order_book_instrument2['best_bid_price'])
                elif instrument_buy_or_sell2 == 'sell' and order_book_instrument2['best_ask_amount'] != 0:
                    best_bid_ask_amount_for_stop_gain_dict2 = float(order_book_instrument2['best_ask_amount'])
                    smaller_amount_for_stop_gain_dic[
                        'best_bid_ask_amount_for_stop_gain_dict2'] = number_multiple_10_and_round_0_digits(
                        abs(float(best_bid_ask_amount_for_stop_gain_dict2)))
                    best_bid_ask_price_for_stop_gain_dict2 = float(order_book_instrument2['best_ask_price'])
                else:
                    best_bid_ask_amount_for_stop_gain_dict2 = 0
                    smaller_amount_for_stop_gain_dic[
                        'best_bid_ask_amount_for_stop_gain_dict2'] = number_multiple_10_and_round_0_digits(
                        abs(float(best_bid_ask_amount_for_stop_gain_dict2)))
                    best_bid_ask_price_for_stop_gain_dict2 = 0

                if len(smaller_amount_for_stop_gain_dic) > 0:
                    smaller_amount_for_stop_gain_name = min(
                        smaller_amount_for_stop_gain_dic, key=smaller_amount_for_stop_gain_dic.get)  # name
                    smaller_amount_for_stop_gain = smaller_amount_for_stop_gain_dic.get(
                        smaller_amount_for_stop_gain_name, 0)  # Valor
                else:
                    smaller_amount_for_stop_gain = 0  # valor                    
                # Args modifically - smaller_amount_dic_for_stop_gain - start ******************************************
                
                # there_are_bid_ask_offer - start **********************************************************************
                if number_multiple_10_and_round_0_digits(best_bid_ask_amount1) >= 10 and \
                        number_multiple_10_and_round_0_digits(best_bid_ask_amount2) >= 10:
                    there_are_bid_ask_offer = True
                else:
                    there_are_bid_ask_offer = False
                    list_monitor_log.append(' ****** There  is NO bid or ask offer ***** ')
                    list_monitor_log.append(
                        instrument_name_1 + ' : ' + str(best_bid_ask_amount1) + ' bid/ask amount ')
                    list_monitor_log.append(
                        instrument_name_2 + ' : ' + str(best_bid_ask_amount2) + ' bid/ask amount ')
                    time.sleep(3)
                # there_are_bid_ask_offer - the end ********************************************************************

                # stop_loss and stop_gain_conditions_trade - start *****************************************************
                if abs(instrument_position1) >= 10 and abs(instrument_position2) >= 10 and \
                        there_are_bid_ask_offer is True and check_instruments_positions_true_or_false is False:
                    stop_loss_for_arbitrage_strategy = stop_loss(set_stop_loss_in_=set_stop_loss_in_,
                                                                 set_stop_loss_value_=set_stop_loss_value_,
                                                                 order_book_instrument1=order_book_instrument1,
                                                                 order_book_instrument2=order_book_instrument2,
                                                                 summary_instrument1=summary_instrument1,
                                                                 summary_instrument2=summary_instrument2)

                    if stop_loss_for_arbitrage_strategy is False:
                        stop_gain_conditions_trade = stop_gain(
                            instrument_name_1=instrument_name_1,
                            instrument_name_2=instrument_name_2,
                            summary_instrument1=summary_instrument1,
                            summary_instrument2=summary_instrument2,
                            order_book_instrument1=order_book_instrument1,
                            order_book_instrument2=order_book_instrument2,
                            set_exit_position_in_=set_exit_position_in_,
                            set_exit_position_bigger_lower_=set_exit_position_bigger_lower_,
                            set_exit_position_value_=set_exit_position_value_
                        )
                    else:
                        stop_gain_conditions_trade = False
                else:
                    stop_loss_for_arbitrage_strategy = False
                    stop_gain_conditions_trade = False

                    # stop loss close postions orders - start **********************************************************
                if stop_loss_for_arbitrage_strategy is True:
                    while instrument_position1 != 0 or instrument_position2 != 0:
                        summary_instrument1 = connect.get_position(instrument_name=instrument_name_1)
                        summary_instrument2 = connect.get_position(instrument_name=instrument_name_2)
                        instrument_position1 = float(summary_instrument1['size'])
                        instrument_position2 = float(summary_instrument2['size'])
                        order_book_instrument1 = connect.get_order_book(instrument_name=instrument_name_1)
                        order_book_instrument2 = connect.get_order_book(instrument_name=instrument_name_2)

                        # Args modifically - smaller_amount_dic and instrument_price1 and instrument_price2 - start ****
                        smaller_amount_dic = dict()
                        smaller_amount_dic.clear()
                        # position current
                        smaller_amount_dic['abs(instrument_position1)'] = \
                            number_multiple_10_and_round_0_digits(abs(instrument_position1))
                        smaller_amount_dic['abs(instrument_position2)'] = \
                            number_multiple_10_and_round_0_digits(abs(instrument_position2))

                        if summary_instrument1['direction'] == 'buy' and order_book_instrument1['best_bid_amount'] != 0:
                            best_bid_ask_amount1 = float(order_book_instrument1['best_bid_amount'])
                            best_bid_ask_price1 = float(order_book_instrument1['best_bid_price'])
                            number_instrument1 = best_bid_ask_price1 - 0.6 * best_bid_ask_price1 / 100
                            instrument_price1 = round(float(number_instrument1 - (number_instrument1 % 0.5)), 2)
                        elif summary_instrument1['direction'] == 'sell' and \
                                order_book_instrument1['best_ask_amount'] != 0:
                            best_bid_ask_amount1 = float(order_book_instrument1['best_ask_amount'])
                            best_bid_ask_price1 = float(order_book_instrument1['best_ask_price'])
                            number_instrument1 = best_bid_ask_price1 + 0.6 * best_bid_ask_price1 / 100
                            instrument_price1 = round(float(number_instrument1 - (number_instrument1 % 0.5)), 2)
                        else:
                            best_bid_ask_amount1 = 0
                            best_bid_ask_price1 = 0
                            instrument_price1 = 0

                        if summary_instrument2['direction'] == 'buy' and order_book_instrument1['best_bid_amount'] != 0:
                            best_bid_ask_amount2 = float(order_book_instrument2['best_bid_amount'])
                            best_bid_ask_price2 = float(order_book_instrument2['best_bid_price'])
                            number_instrument2 = best_bid_ask_price2 - 0.6 * best_bid_ask_price2 / 100
                            instrument_price2 = round(float(number_instrument2 - (number_instrument2 % 0.5)), 2)
                        elif summary_instrument2['direction'] == 'sell' and \
                                order_book_instrument1['best_ask_amount'] != 0:
                            best_bid_ask_amount2 = float(order_book_instrument2['best_ask_amount'])
                            best_bid_ask_price2 = float(order_book_instrument2['best_ask_price'])
                            number_instrument2 = best_bid_ask_price2 + 0.6 * best_bid_ask_price2 / 100
                            instrument_price2 = round(float(number_instrument2 - (number_instrument2 % 0.5)), 2)
                        else:
                            best_bid_ask_amount2 = 0
                            best_bid_ask_price2 = 0
                            instrument_price2 = 0

                        smaller_amount_dic['best_bid_ask_amount1'] = number_multiple_10_and_round_0_digits(
                            abs(float(best_bid_ask_amount1))
                        )
                        smaller_amount_dic['best_bid_ask_amount2'] = number_multiple_10_and_round_0_digits(
                            abs(float(best_bid_ask_amount2))
                        )

                        if len(smaller_amount_dic) > 0:
                            smaller_amount_name = min(smaller_amount_dic, key=smaller_amount_dic.get)  # name
                            smaller_amount_for_stop_orders = smaller_amount_dic.get(smaller_amount_name, 0)  # Valor
                        else:
                            smaller_amount_for_stop_orders = 0  # valor
                        # Args modifically - smaller_amount_dic and instrument_price1 and instrument_price2 - the end **

                        smaller_amount_for_stop_orders = number_multiple_10_and_round_0_digits(
                            smaller_amount_for_stop_orders)
                        if smaller_amount_for_stop_orders >= 10 and \
                                best_bid_ask_price1 != 0 and \
                                best_bid_ask_price2 != 0 and \
                                instrument_price1 != 0 and \
                                instrument_price2 != 0:

                            if summary_instrument1['direction'] == 'buy':
                                connect.sell_limit(
                                    currency=instrument_name_1,
                                    amount=smaller_amount_for_stop_orders,
                                    price=instrument_price1)
                                connect.buy_limit(
                                    currency=instrument_name_2,
                                    amount=smaller_amount_for_stop_orders,
                                    price=instrument_price2)
                                list_monitor_log.append(' *** STOP LOSS ORDERS: *** ')
                                list_monitor_log.append(
                                    'currency: ' + instrument_name_1 +
                                    'order: sell limit' +
                                    'amount: ' + str(smaller_amount_for_stop_orders) +
                                    'price :' + str(instrument_price1) + ' ')
                                list_monitor_log.append(
                                    'currency: ' + instrument_name_2 +
                                    'order: buy limit' +
                                    'amount: ' + str(smaller_amount_for_stop_orders) +
                                    'price :' + str(instrument_price2) + ' ')
                                connect.logwriter(' *** STOP LOSS ORDERS: *** ')
                                connect.logwriter(
                                    'currency: ' + instrument_name_1 +
                                    'order: sell limit' +
                                    'amount: ' + str(smaller_amount_for_stop_orders) +
                                    'price :' + str(instrument_price1) + ' ')
                                connect.logwriter(
                                    'currency: ' + instrument_name_2 +
                                    'order: sell limit' +
                                    'amount: ' + str(smaller_amount_for_stop_orders) +
                                    'price :' + str(instrument_price2) + ' ')
                                time.sleep(5)
                                connect.cancel_all()
                            else:
                                connect.buy_limit(
                                    currency=instrument_name_1,
                                    amount=smaller_amount_for_stop_orders,
                                    price=instrument_price1)
                                connect.sell_limit(
                                    currency=instrument_name_2,
                                    amount=smaller_amount_for_stop_orders,
                                    price=instrument_price2)
                                list_monitor_log.append(' *** STOP LOSS ORDERS: *** ')
                                list_monitor_log.append(
                                    'currency: ' + instrument_name_1 +
                                    'order: buy limit' +
                                    'amount: ' + str(smaller_amount_for_stop_orders) +
                                    'price :' + str(instrument_price1) + ' ')
                                list_monitor_log.append(
                                    'currency: ' + instrument_name_2 +
                                    'order: sell limit' +
                                    'amount: ' + str(smaller_amount_for_stop_orders) +
                                    'price :' + str(instrument_price2) + ' ')
                                connect.logwriter(' *** STOP LOSS ORDERS: *** ')
                                connect.logwriter(
                                    'currency: ' + instrument_name_1 +
                                    'order: buy limit' +
                                    'amount: ' + str(smaller_amount_for_stop_orders) +
                                    'price :' + str(instrument_price1) + ' ')
                                connect.logwriter(
                                    'currency: ' + instrument_name_2 +
                                    'order: sell limit' +
                                    'amount: ' + str(smaller_amount_for_stop_orders) +
                                    'price :' + str(instrument_price2) + ' ')
                                time.sleep(5)
                                connect.cancel_all()
                        else:
                            connect.close_position(instrument_name=instrument_name_1)
                            connect.close_position(instrument_name=instrument_name_2)
                            list_monitor_log.append(' *** STOP LOSS ORDERS: *** ')
                            list_monitor_log.append(
                                'currency: ' + instrument_name_1 + instrument_name_2 +
                                'order: close position ')
                            connect.logwriter('\n*** STOP LOSS ORDERS: ***')
                            connect.logwriter(
                                '\ncurrency: ' + instrument_name_1 + instrument_name_2 +
                                'order: close position ')
                            time.sleep(5)
                            connect.cancel_all()
                else:
                    pass  # stop_loss_for_arbitrage_strategy is False
                    # stop loss close positions orders - the end *******************************************************

                    # stop_loss_counter - start ************************************************************************
                if stop_loss_for_arbitrage_strategy is True:
                    stop_loss_counter = stop_loss_counter + 1
                else:
                    pass

                if stop_loss_counter >= 2:
                    list_monitor_log.append(' *** Stop Loss Counter: ' + str(stop_loss_counter) + ' *** ')
                    connect.logwriter('\n*** Stop Loss Counter: ' + str(stop_loss_counter) + ' ***')
                    # stop_loss_counter - the end **********************************************************************
                # stop_loss_conditions_trade and stop_gain_conditions_trade - the end **********************************

                # stop gain orders - start *****************************************************************************                
                if stop_gain_conditions_trade is True and \
                        there_are_bid_ask_offer is True and \
                        stop_loss_counter < 2 and \
                        stop_loss_for_arbitrage_strategy is False and \
                        number_multiple_10_and_round_0_digits(abs(instrument_position1)) >= 10 and \
                        number_multiple_10_and_round_0_digits(abs(instrument_position2)) >= 10 and \
                        best_bid_ask_amount_for_stop_gain_dict1 != 0 and \
                        best_bid_ask_amount_for_stop_gain_dict2 != 0 and \
                        check_instruments_positions_true_or_false is False:

                    smaller_amount_for_stop_gain_orders = smaller_amount_for_stop_gain
                    smaller_amount_for_stop_gain_orders = number_multiple_10_and_round_0_digits(
                        smaller_amount_for_stop_gain_orders)
                    if smaller_amount_for_stop_gain_orders >= 10 and best_bid_ask_price_for_stop_gain_dict1 != 0 and \
                            best_bid_ask_price_for_stop_gain_dict2 != 0:
                        if summary_instrument1['direction'] == 'buy':
                            connect.sell_limit(
                                currency=instrument_name_1,
                                amount=smaller_amount_for_stop_gain_orders,
                                price=best_bid_ask_price_for_stop_gain_dict1)
                            connect.buy_limit(
                                currency=instrument_name_2,
                                amount=smaller_amount_for_stop_gain_orders,
                                price=best_bid_ask_price_for_stop_gain_dict2)
                            list_monitor_log.append(' *** STOP GAIN ORDERS SENT: *** ')
                            list_monitor_log.append(
                                'currency: ' + instrument_name_1 +
                                'order: sell limit' +
                                'amount: ' + str(smaller_amount_for_stop_gain_orders) +
                                'price :' + str(best_bid_ask_price_for_stop_gain_dict1) + ' ')
                            list_monitor_log.append(
                                'currency: ' + instrument_name_2 +
                                'order: buy limit' +
                                'amount: ' + str(smaller_amount_for_stop_gain_orders) +
                                'price :' + str(best_bid_ask_price_for_stop_gain_dict2) + ' ')
                            connect.logwriter('\n*** STOP GAIN ORDERS SENT: *** ')
                            connect.logwriter(
                                '\ncurrency: ' + instrument_name_1 +
                                'order: sell limit' +
                                'amount: ' + str(smaller_amount_for_stop_gain_orders) +
                                'price :' + str(best_bid_ask_price_for_stop_gain_dict1) + ' ')
                            connect.logwriter(
                                '\ncurrency: ' + instrument_name_2 +
                                'order: buy limit' +
                                'amount: ' + str(smaller_amount_for_stop_gain_orders) +
                                'price :' + str(best_bid_ask_price_for_stop_gain_dict2))
                            time.sleep(5)
                            connect.cancel_all()
                        elif summary_instrument1['direction'] == 'sell':
                            connect.buy_limit(
                                currency=instrument_name_1,
                                amount=smaller_amount_for_stop_gain_orders,
                                price=best_bid_ask_price_for_stop_gain_dict1)
                            connect.sell_limit(
                                currency=instrument_name_2,
                                amount=smaller_amount_for_stop_gain_orders,
                                price=best_bid_ask_price_for_stop_gain_dict2)
                            list_monitor_log.append(' *** STOP GAIN ORDERS SENT: *** ')
                            list_monitor_log.append(
                                'currency: ' + instrument_name_1 +
                                'order: buy limit' +
                                'amount: ' + str(smaller_amount_for_stop_gain_orders) +
                                'price :' + str(best_bid_ask_price_for_stop_gain_dict1) + ' ')
                            list_monitor_log.append(
                                'currency: ' + instrument_name_2 +
                                'order: sell limit' +
                                'amount: ' + str(smaller_amount_for_stop_gain_orders) +
                                'price :' + str(best_bid_ask_price_for_stop_gain_dict2) + ' ')
                            connect.logwriter('\n *** STOP GAIN ORDERS SENT: *** ')
                            connect.logwriter(
                                '\ncurrency: ' + instrument_name_1 +
                                'order: buy limit' +
                                'amount: ' + str(smaller_amount_for_stop_gain_orders) +
                                'price :' + str(best_bid_ask_price_for_stop_gain_dict1))
                            connect.logwriter(
                                '\ncurrency: ' + instrument_name_2 +
                                'order: sell limit' +
                                'amount: ' + str(smaller_amount_for_stop_gain_orders) +
                                'price :' + str(best_bid_ask_price_for_stop_gain_dict2))
                            time.sleep(5)
                            connect.cancel_all()
                        else:
                            list_monitor_log.append('***** ERROR IN STOP GAIN ORDERS - Error Code: 2419 ***')
                            connect.logwriter('\n***** ERROR IN STOP GAIN ORDERS - Error Code: 2420 ***')
                        time.sleep(2)
                    else:                        
                        list_monitor_log.append(' *** Smaller amount for stop gain order < 10 USD *** ')
                else:
                    pass  # stop_gain_conditions_trade is True                
                # stop gain orders - the end ***************************************************************************

                # open_conditions_trade - start ************************************************************************
                if there_are_bid_ask_offer is True and \
                        stop_gain_conditions_trade is False and \
                        stop_loss_counter < 2 and \
                        stop_loss_for_arbitrage_strategy is False and \
                        number_multiple_10_and_round_0_digits(
                            (abs(total_amount) / 2) - abs(instrument_position1)) >= 10 and \
                        number_multiple_10_and_round_0_digits(
                            (abs(total_amount) / 2) - abs(instrument_position2)) >= 10 and \
                        number_multiple_10_and_round_0_digits(
                            abs(total_amount) - (abs(instrument_position1) + abs(instrument_position2))) >= 10 and \
                        abs(instrument_position1) <= abs(instrument_amount1_usd_before_trade) - 10 and \
                        abs(instrument_position2) <= abs(instrument_amount2_usd_before_trade) - 10 and \
                        check_instruments_positions_true_or_false is False:

                    open_conditions_trade = strategy_entry(
                        instrument_name_1=instrument_name_1,
                        instrument_name_2=instrument_name_2,
                        best_bid_ask_price_in_usd_instrument1=best_bid_ask_price1,
                        best_bid_ask_price_in_usd_instrument2=best_bid_ask_price2,
                        set_entry_position_in_=set_entry_position_in_,
                        set_entry_position_bigger_lower_=set_entry_position_bigger_lower_,
                        set_entry_position_value_=set_entry_position_value_
                    )
                else:
                    open_conditions_trade = False
                # open_conditions_trade - the end **********************************************************************

                # open_trade_orders - start ****************************************************************************
                if open_conditions_trade is True and \
                        stop_gain_conditions_trade is False and \
                        stop_loss_for_arbitrage_strategy is False and \
                        stop_loss_counter < 2 and \
                        there_are_bid_ask_offer is True and \
                        positions_with_same_size_in_usd_or_currency == 'USD' and \
                        number_multiple_10_and_round_0_digits(
                            abs(instrument_amount1_usd_before_trade) - abs(instrument_position1)) >= 10 > abs(
                            abs(instrument_position1) - abs(instrument_position2)) and \
                        number_multiple_10_and_round_0_digits(abs(
                            instrument_amount2_usd_before_trade) - abs(instrument_position2)) >= 10 and \
                        number_multiple_10_and_round_0_digits(smaller_amount) >= 10 and \
                        best_bid_ask_price1 != 0 and \
                        best_bid_ask_price2 != 0 and \
                        best_bid_ask_amount1 != 0 and \
                        best_bid_ask_amount2 != 0 and \
                        check_instruments_positions_true_or_false is False:

                    instrument1_amount_order_usd_for_open_orders = number_multiple_10_and_round_0_digits(
                        abs(float(smaller_amount)))
                    instrument2_amount_order_usd_for_open_orders = instrument1_amount_order_usd_for_open_orders

                    if instrument_buy_or_sell1 == 'buy' and instrument_buy_or_sell2 == 'sell':
                        connect.buy_limit(
                            currency=instrument_name_1,
                            amount=instrument1_amount_order_usd_for_open_orders,
                            price=best_bid_ask_price1)
                        connect.sell_limit(
                            currency=instrument_name_2,
                            amount=instrument2_amount_order_usd_for_open_orders,
                            price=best_bid_ask_price2)
                        list_monitor_log.append(' *** OPENING ORDERS SENT: *** ')
                        list_monitor_log.append(
                            'currency: ' + instrument_name_1 +
                            'order: buy limit' +
                            'amount: ' + str(instrument1_amount_order_usd_for_open_orders) +
                            'price :' + str(best_bid_ask_price1) + ' ')
                        list_monitor_log.append(
                            'currency: ' + instrument_name_2 +
                            'order: sell limit' +
                            'amount: ' + str(instrument2_amount_order_usd_for_open_orders) +
                            'price :' + str(best_bid_ask_price2) + ' ')
                        connect.logwriter('\n*** OPENING ORDERS SENT: ***')
                        connect.logwriter(
                            '\ncurrency: ' + instrument_name_1 +
                            'order: buy limit' +
                            'amount: ' + str(instrument1_amount_order_usd_for_open_orders) +
                            'price :' + str(best_bid_ask_price1) + ' ')
                        connect.logwriter(
                            '\ncurrency: ' + instrument_name_2 +
                            'order: sell limit' +
                            'amount: ' + str(instrument2_amount_order_usd_for_open_orders) +
                            'price :' + str(best_bid_ask_price2))
                        time.sleep(5)
                        connect.cancel_all()

                    elif instrument_buy_or_sell1 == 'sell' and instrument_buy_or_sell2 == 'buy':
                        connect.sell_limit(
                            currency=instrument_name_1,
                            amount=instrument1_amount_order_usd_for_open_orders,
                            price=best_bid_ask_price1)
                        connect.buy_limit(
                            currency=instrument_name_2,
                            amount=instrument2_amount_order_usd_for_open_orders,
                            price=best_bid_ask_price2)
                        list_monitor_log.append(' *** OPENING ORDERS SENT: *** ')
                        list_monitor_log.append(
                            'currency: ' + instrument_name_1 +
                            'order: sell limit' +
                            'amount: ' + str(instrument1_amount_order_usd_for_open_orders) +
                            'price :' + str(best_bid_ask_price1) + ' ')
                        list_monitor_log.append(
                            'currency: ' + instrument_name_2 +
                            'order: buy limit' +
                            'amount: ' + str(instrument2_amount_order_usd_for_open_orders) +
                            'price :' + str(best_bid_ask_price2) + ' ')
                        connect.logwriter('\n*** OPENING ORDERS SENT: *** ')
                        connect.logwriter(
                            '\ncurrency: ' + instrument_name_1 +
                            'order: sell limit' +
                            'amount: ' + str(instrument1_amount_order_usd_for_open_orders) +
                            'price :' + str(best_bid_ask_price1))
                        connect.logwriter(
                            '\ncurrency: ' + instrument_name_2 +
                            'order: buy limit' +
                            'amount: ' + str(instrument2_amount_order_usd_for_open_orders) +
                            'price :' + str(best_bid_ask_price2))
                        time.sleep(5)
                        connect.cancel_all()
                    else:
                        list_monitor_log.append(' ***** ERROR OPENING ORDERS SENT - Error Code: 2540 *** ')
                        connect.logwriter('\n***** ERROR OPENING ORDERS SENT - Error Code: 2541 ***')
                    time.sleep(2)
                else:
                    list_monitor_log.append(' *** Opening orders NO sent *** ')
                # open_trade_orders - the end **************************************************************************

                # check_postion1_same_postirion2_in_usd - start ********************************************************
                list_monitor_log.append(' *** Check instruments positions *** ')
                if positions_with_same_size_in_usd_or_currency == 'USD' and \
                        abs(abs(instrument_position1) - abs(instrument_position2)) >= 10 and \
                        there_are_bid_ask_offer is True:

                    check_instruments_positions_true_or_false = True
                    check_instruments_positions(
                        instrument_name_1=instrument_name_1,
                        instrument_name_2=instrument_name_2,
                        positions_with_same_size_in_usd_or_currency=positions_with_same_size_in_usd_or_currency,
                        total_amount=total_amount,
                        instrument_buy_or_sell1=instrument_buy_or_sell1,
                        instrument_buy_or_sell2=instrument_buy_or_sell2)
                else:
                    check_instruments_positions_true_or_false = False
                    list_monitor_log.append(' *** Instruments positions are checked *** ')
                # check_postion1_same_postirion2_in_usd - the end ******************************************************

                # check_postion1_same_postirion2_in_usd if diferente directions or postions > total amount - start *****
                list_monitor_log.append(' *** Check instruments direction *** ')
                if positions_with_same_size_in_usd_or_currency == 'USD' and \
                        (((instrument_buy_or_sell1 != summary_instrument1['direction'] and
                           float(instrument_position1) != 0) or
                            (instrument_buy_or_sell2 != summary_instrument2['direction'] and
                             instrument_position2 != 0)) or
                         abs(float(total_amount / 2)) - abs(float(instrument_position1)) <= -10 or
                         abs(float(total_amount / 2)) - abs(float(instrument_position2)) <= -10 or
                         abs(float(total_amount)) - (abs(float(instrument_position1)) +
                         abs(float(instrument_position2))) <= -10) and \
                        there_are_bid_ask_offer is True:

                    check_instruments_positions_true_or_false = True
                    check_instruments_positions(
                        instrument_name_1=instrument_name_1,
                        instrument_name_2=instrument_name_2,
                        positions_with_same_size_in_usd_or_currency=positions_with_same_size_in_usd_or_currency,
                        total_amount=total_amount,
                        instrument_buy_or_sell1=instrument_buy_or_sell1,
                        instrument_buy_or_sell2=instrument_buy_or_sell2)
                else:
                    check_instruments_positions_true_or_false = False
                    list_monitor_log.append(' *** Instruments directions and postions < total amount are checked *** ')
                # check_postion1_same_postirion2_in_usd if diferente directions or postions > total amount- the end ****

                btc_index_and_greeks_structure_monitor_print()

            except Exception as er:
                list_monitor_log.append(str(er))
                time.sleep(40)
                pass
            finally:
                pass

        info = {
            'object_signal': 'setup_arbitrage_strategy_stopped',
            'msg': ''
        }
        sinal.ui_signal1.emit(info)

        list_monitor_log.append('***** Arbitrage Stopped *****')
        time.sleep(5)

        index_greeks_print_on_off = 'on'
        print_index_and_summary()

    def strategy_off():
        global strategy_on_off
        strategy_on_off = 'off'

    def thread_arbitrage_strategy():
        arbitrage_strategy_thread = threading.Thread(daemon=True, target=arbitrage_strategy())
        arbitrage_strategy_thread.start()

    def start_arbitrage_strategy_and_message():
        global index_greeks_print_on_off

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Start Arbitrage?')
        msg.setWindowTitle('*** WARNING ***')
        msg.addButton('Ok', msg.AcceptRole)
        msg.addButton('Cancel', msg.RejectRole)
        pass
        if msg.exec_() == msg.Rejected:
            index_greeks_print_on_off = 'off'  # ok clicked
        else:
            pass  # cancel clicked

    sinal.ui_signal1.connect(ui_signal1)
    monitor_thread = threading.Thread(daemon=True, target=lists_monitor)
    monitor_thread.start()
    ui.pushButton_start_print_loglog.hide()
    ui.pushButton_2.hide()
    ui.textEdit_monitor.textChanged.connect(autoscroll_monitor)
    monitor_index_and_summary_thread = threading.Thread(daemon=True, target=print_index_and_summary)
    monitor_index_and_summary_thread.start()
    ui.pushButton_start_trading.clicked.connect(start_arbitrage_strategy_and_message)
    ui.pushButton_stop_arbitrage.clicked.connect(strategy_off)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    credentials(ui=ui)
    config(ui=ui)
    run_arbitrage(ui=ui)
    sys.exit(app.exec_())
