#!/usr/bin/python3
import sys, PyQt5, dlg001, configparser, time, threading, socket, translator, webbrowser, os, base64, datetime
import languages.ru_RU as ru_RU
import languages.en_US as en_US
from functools import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from mainform import Ui_MainWindow
from dlg001 import Ui_Dialog as swiz_001
from dlg002 import Ui_Dialog as swiz_002
from dlg003 import Ui_Dialog as swiz_003
from dlg004 import Ui_Dialog as aboutprg
from dlg005 import Ui_Dialog as ext_sett

settings = configparser.ConfigParser()
profiles = configparser.ConfigParser()

version = '0.2.0 Beta'
date = '2021-08-27'
now = datetime.datetime.now()

enckey = Fernet.generate_key()
fernet = Fernet(enckey)

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

class Thread(QThread):
    logged = QtCore.pyqtSignal(str, str, float, str, str, str, float, socket.socket)
    started = QtCore.pyqtSignal(str, str, float, str, str, str, float, socket.socket)

    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.parent = parent
    def run(self):
            profiles.read('profiles')
            if profiles.sections() != [] or profiles.sections() != None and (profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['server'] != '' and profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['port'] != '') and (profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['nicknames'] != '' and profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['nicknames'] != ''):
                self.encoding = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Encoding']
                self.username = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Nicknames'].split(', ')[0]
                self.server = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Server']
                self.port = int(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Port'])
                self.channel = ""
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.quiting_msg = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['quitingmsg']
                fernet = Fernet(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['EncryptCode'].encode('UTF-8'))
                self.password = fernet.decrypt(bytes(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Password'], 'UTF-8')).decode(self.encoding)
                try:
                    self.until_ping = time.time()
                    threshold = 1 * 60
                    self.ping = time.time()
                    self.socket.connect((self.server,self.port))
                    print('Connecting to {0}...'.format(self.server))
                    self.socket.setblocking(True)
                    self.socket.send(bytes("USER " + self.username + " " + self.username +" " + self.username + " :Testing\n", self.encoding))
                    self.socket.send(bytes("NICK " + self.username + "\n", self.encoding))

                    while True:
                        self.text=self.socket.recv(2040)
                        self.ping = time.time()
                        self.started.emit(''.join(self.text.decode(self.encoding).split(":")), self.server, self.port, self.username, self.encoding, self.quiting_msg, self.ping, self.socket)
                        msg_list = self.text.decode(self.encoding).splitlines()
                        for msg_line in msg_list:
                            if msg_line.startswith('PING :'):
                                ping_msg = msg_line.split(' ')
                                self.socket.send(bytes('PONG {0}\r\n'.format(ping_msg[1]), self.encoding))
                                self.started.emit('PONG', self.server, self.port, self.username, self.encoding, self.quiting_msg, self.ping, self.socket)

                    if profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['AuthMethod'] == 'NickServ' and profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Password'] != '':
                        self.socket.send(bytes("PRIVMSG nickserv identify {0} {1}\r\n".format(self.username, self.password), self.encoding))
                except Exception as e:
                    print('Exception: {0}'.format(e))
                    self.started.emit('Exception: {0}'.format(str(e)), self.server, self.port, self.username, self.encoding, self.quiting_msg, self.ping, self.socket)
                    self.socket.close()

    def kill(self):
        self.quit()

class mainform(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainform, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.conn_quality_progr.setValue(0)
        self.ui.latency_label.setText("")
        self.child = SettingsWizard001(self)
        self.child_2 = SettingsWizard002()
        self.child_3 = SettingsWizard003()
        self.child_4 = AboutProgramDlg()
        self.child_5 = AdvancedSettingsDlg()
        self.ui.about_item.triggered.connect(self.about_window)
        self.ui.connect_item.triggered.connect(self.connect_window)
        self.ui.settings_item.triggered.connect(self.settings_window)
        self.ui.quit_item.triggered.connect(self.quit_app)
        settings.read('settings')
        profiles.read('profiles')
        print('Tinelix codename Flight {0} ({1})\nDone!'.format(version, date))
        self.ui.dialogs_list.setVisible(False)
        self.ui.members_list.setVisible(False)

        if settings.sections() == []:
            settings['Main'] = {'Language': 'Russian', 'ColorScheme': 'Orange', 'DarkTheme': 'True', 'MsgHistory': 'True', 'MessagesHint': 'False'}
            with open('settings', 'w') as configfile:
                settings.write(configfile)
        else:
            translator.translate_001(self, self.child.ui, settings['Main']['Language'], en_US, ru_RU)
            if settings['Main']['DarkTheme'] == 'Disabled':
                self.ui.line.setStyleSheet('color: #afafaf')
                self.child.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
                self.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
                self.ui.menubar.setStyleSheet('selection-background-color: #ff7700; selection-color: #000000')
                self.ui.conn_quality_progr.setStyleSheet('selection-background-color: #ff7700')
                self.ui.chat_text.setStyleSheet('selection-background-color: #ff7700')
                self.ui.members_list.setStyleSheet('selection-background-color: #ff7700')
                if self.ui.message_text.isEnabled() == True:
                    self.ui.message_text.setStyleSheet('selection-background-color: #ff7700')
            else:
                self.ui.line.setStyleSheet('color: #4a4a4a')
                self.child.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
                self.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
                self.ui.menubar.setStyleSheet('selection-background-color: #a14b00; selection-color: #ffffff')
                self.ui.conn_quality_progr.setStyleSheet('selection-background-color: #a14b00')
                self.ui.chat_text.setStyleSheet('selection-background-color: #a14b00')
                self.ui.members_list.setStyleSheet('selection-background-color: #a14b00')
                if self.ui.message_text.isEnabled() == True:
                    self.ui.message_text.setStyleSheet('selection-background-color: #a14b00')

        #swiz001 = SettingsWizard001()
        self.child.show()
        if settings['Main']['DarkTheme'] == 'Disabled':
            self.child.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            self.child.ui.tableWidget.setStyleSheet('border-color: #ff7700; selection-background-color: #ff7700')
            self.child.ui.language_combo.setStyleSheet('border-color: #ff7700; selection-background-color: #ff7700')
        else:
            self.child.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            self.child.ui.tableWidget.setStyleSheet('border-color: #ff7700; selection-background-color: #a14b00')
            self.child.ui.language_combo.setStyleSheet('border-color: #ff7700; selection-background-color: #a14b00')
        try:
            self.child.ui.language_combo.setCurrentText(settings['Main']['Language'])
        except Exception as e:
            print(e)
        self.child.ui.language_combo.currentIndexChanged.connect(self.change_language)

    def change_language(self):
        index = self.child.ui.language_combo.currentIndex()
        print(index)
        try:
            if index == 0:
                settings['Main']['Language'] = 'Russian'
                with open('settings', 'w') as configfile:
                    settings.write(configfile)
                translator.translate_001(self, self.child.ui, 'Russian', en_US, ru_RU)
            else:
                settings['Main']['Language'] = 'English'
                with open('settings', 'w') as configfile:
                    settings.write(configfile)
                translator.translate_001(self, self.child.ui, 'English', en_US, ru_RU)
            settings.read('settings')
        except Exception as e:
            print('Exception: {0}'.format(e))
        index_5 = self.child_5.ui.language_combo.currentIndex()
        try:
            if index_5 == 0:
                settings['Main']['Language'] = 'Russian'
                with open('settings', 'w') as configfile:
                    settings.write(configfile)
                translator.translate_005(self, self.child_5.ui, 'Russian', en_US, ru_RU)
            else:
                settings['Main']['Language'] = 'English'
                with open('settings', 'w') as configfile:
                    settings.write(configfile)
                translator.translate_005(self, self.child_5.ui, 'English', en_US, ru_RU)
            settings.read('settings')
        except Exception as e:
            print('Exception: {0}'.format(e))

    def about_window(self):
        settings.read('settings')
        self.version = version
        if settings.sections() == []:
            settings['Main'] = {'Language': 'Russian', 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'True', 'MessagesHint': 'False'}
            with open('settings', 'w') as configfile:
                settings.write(configfile)
            translator.translate_004(self, self.child_4.ui, 'Russian', en_US, ru_RU)
        else:
            translator.translate_004(self, self.child_4.ui, settings['Main']['Language'], en_US, ru_RU)
            if settings['Main']['DarkTheme'] == 'Disabled':
                self.child_4.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            else:
                self.child_4.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
        self.child_4.exec_()


    def settings_window(self):
        settings.read('settings')
        self.version = version
        if settings.sections() == []:
            settings['Main'] = {'Language': 'Russian', 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'True', 'MessagesHint': 'False'}
            with open('settings', 'w') as configfile:
                settings.write(configfile)
            translator.translate_005(self, self.child_5.ui, 'Russian', en_US, ru_RU)
        else:
            translator.translate_005(self, self.child_5.ui, settings['Main']['Language'], en_US, ru_RU)
            if settings['Main']['DarkTheme'] == 'Disabled':
                self.child_5.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
                self.child_5.ui.dark_theme_cb.setCheckState(0)
            else:
                self.child_5.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
                self.child_5.ui.dark_theme_cb.setCheckState(2)
            if settings['Main']['MsgHistory'] == 'Disabled':
                self.child_5.ui.save_msghistory_cb.setCheckState(0)
            else:
                self.child_5.ui.save_msghistory_cb.setCheckState(2)
        self.child_5.ui.language_combo.clear()
        self.child_5.ui.language_combo.addItem('English')
        self.child_5.ui.language_combo.addItem('Russian')
        try:
            self.child_5.ui.language_combo.setCurrentText(settings['Main']['Language'])
        except Exception as e:
            print(e)
        self.child_5.ui.language_combo.currentIndexChanged.connect(self.change_language)
        self.child_5.ui.buttonBox.accepted.connect(self.save_settings)
        self.child_5.ui.dark_theme_cb.stateChanged.connect(self.change_theme)
        self.child_5.exec_()

    def change_theme(self):
        if self.child_5.ui.dark_theme_cb.checkState() == False:
            self.child_5.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            self.ui.line.setStyleSheet('color: #afafaf')
            self.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            self.ui.menubar.setStyleSheet('selection-background-color: #ff7700; selection-color: #000000')
            self.ui.conn_quality_progr.setStyleSheet('selection-background-color: #ff7700')
            self.ui.chat_text.setStyleSheet('selection-background-color: #ff7700')
            self.ui.members_list.setStyleSheet('selection-background-color: #ff7700')
            if self.ui.message_text.isEnabled() == True:
                self.ui.message_text.setStyleSheet('selection-background-color: #ff7700')
            try:
                self.child.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
                self.child.ui.tableWidget.setStyleSheet('selection-background-color: #ff7700; selection-color: #000000')
                if self.child.ui.change_profile_btn.isEnabled() == True:
                    self.child.ui.change_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
                if self.child.ui.connect_btn.isEnabled() == True:
                    self.child.ui.connect_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
                    self.child.ui.del_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
            except:
                pass
        else:
            self.child_5.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            self.ui.line.setStyleSheet('color: #4a4a4a')
            self.child.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            self.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            self.ui.menubar.setStyleSheet('selection-background-color: #a14b00; selection-color: #ffffff')
            self.ui.conn_quality_progr.setStyleSheet('selection-background-color: #a14b00')
            self.ui.chat_text.setStyleSheet('selection-background-color: #a14b00')
            self.ui.members_list.setStyleSheet('selection-background-color: #a14b00')
            if self.ui.message_text.isEnabled() == True:
                self.ui.message_text.setStyleSheet('selection-background-color: #a14b00')
            try:
                self.child.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
                self.child.ui.tableWidget.setStyleSheet('selection-background-color: #ff7700; selection-color: #000000')
                if self.child.ui.change_profile_btn.isEnabled() == True:
                    self.child.ui.change_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
                if self.child.ui.connect_btn.isEnabled() == True:
                    self.child.ui.connect_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
                    self.child.ui.del_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
                self.child.ui.tableWidget.setStyleSheet('selection-background-color: #a14b00')
            except:
                pass

    def save_settings(self):
        try:
            if self.child_5.ui.dark_theme_cb.checkState() == 0:
                if self.child_5.ui.save_msghistory_cb.checkState() == 0:
                    if self.child_5.ui.msgs_hint.checkState() == 0:
                        settings['Main'] = {'Language': self.child_5.ui.language_combo.currentText(), 'ColorScheme': 'Orange', 'DarkTheme': 'Disabled', 'MsgHistory': 'Disabled', 'MessagesHint': 'Enabled'}
                    else:
                        settings['Main'] = {'Language': self.child_5.ui.language_combo.currentText(), 'ColorScheme': 'Orange', 'DarkTheme': 'Disabled', 'MsgHistory': 'Disabled', 'MessagesHint': 'Disabled'}
                else:
                    if self.child_5.ui.msgs_hint.checkState() == 0:
                        settings['Main'] = {'Language': self.child_5.ui.language_combo.currentText(), 'ColorScheme': 'Orange', 'DarkTheme': 'Disabled', 'MsgHistory': 'Enabled', 'MessagesHint': 'Enabled'}
                    else:
                        settings['Main'] = {'Language': self.child_5.ui.language_combo.currentText(), 'ColorScheme': 'Orange', 'DarkTheme': 'Disabled', 'MsgHistory': 'Enabled', 'MessagesHint': 'Disabled'}
            else:
                if self.child_5.ui.save_msghistory_cb.checkState() == 0:
                    if self.child_5.ui.msgs_hint.checkState() == 0:
                        settings['Main'] = {'Language': self.child_5.ui.language_combo.currentText(), 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'Disabled', 'MessagesHint': 'Enabled'}
                    else:
                        settings['Main'] = {'Language': self.child_5.ui.language_combo.currentText(), 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'Disabled', 'MessagesHint': 'Disabled'}
                else:
                    if self.child_5.ui.msgs_hint.checkState() == 0:
                        settings['Main'] = {'Language': self.child_5.ui.language_combo.currentText(), 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'Enabled', 'MessagesHint': 'Enabled'}
                    else:
                        settings['Main'] = {'Language': self.child_5.ui.language_combo.currentText(), 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'Enabled', 'MessagesHint': 'Disabled'}
            with open('settings', 'w') as configfile:
                settings.write(configfile)
        except:
            pass

    def connect_window(self):
        self.child.ui.language_label.setVisible(False)
        self.child.ui.language_combo.setVisible(False)
        if settings['Main']['DarkTheme'] == 'Disabled':
            self.child.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
        else:
            self.child.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
        self.child.exec_()

    def quit_app(self):
        print('Quiting...')
        self.close()

class SettingsWizard003(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.ui = swiz_003()
        self.ui.setupUi(self)
        settings.read('settings')
        self.ui.buttonBox.accepted.connect(self.save_profile)
        self.ui.buttonBox.accepted.connect(self.save_profile)
        self.ui.clear_nicknames_btn.clicked.connect(self.clear_nicknames)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(100)
        if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
            self.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
        else:
            self.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')

    def tick(self):
        self.ui.nicknames_combo.currentIndexChanged.connect(self.show_create_nickname_dlg)
        if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
            self.setStyleSheet('background-color: #ffffff; color: #000000;')
            self.ui.profname_box.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
            self.ui.nicknames_combo.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
            self.ui.authmethod_combo.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
            self.ui.nicknames_combo.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
            self.ui.password_box.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
            self.ui.server_box.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
            self.ui.port_box.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
            self.ui.encoding_combo.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
            self.ui.quiting_msg_box.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
        elif settings.sections() != [] and settings['Main']['DarkTheme'] == 'Enabled':
            self.setStyleSheet('background-color: #313131; color: #ffffff;')
            self.ui.profname_box.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
            self.ui.authmethod_combo.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
            self.ui.nicknames_combo.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
            self.ui.password_box.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
            self.ui.server_box.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
            self.ui.port_box.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
            self.ui.encoding_combo.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
            self.ui.quiting_msg_box.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
        self.timer.stop()

    def show_create_nickname_dlg(self):
        index = self.ui.nicknames_combo.currentIndex()
        if index == self.ui.nicknames_combo.count() - 1:
            self.close()
            swiz002 = SettingsWizard002()
            if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                swiz002.ui.label.setText(ru_RU.get()['chnicknm'])
            elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                swiz002.ui.label.setText(en_US.get()['chnicknm'])
            else:
                swiz002.ui.label.setText(ru_RU.get()['chnicknm'])
            swiz002.ui.profname.setText(self.ui.profname_box.text())
            swiz002.exec_()

    def add_nickname(self):
        self.ui.nicknames_combo.addItem(self.ui.lineEdit.text())

    def save_profile(self):
        try:
            profiles.read('profiles')
            nicknames_list = []
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=os.urandom(16),
                iterations=100000
            )
            encrypt_code = base64.urlsafe_b64encode(kdf.derive(bytes(self.ui.password_box.text(), 'UTF-8')))
            fernet = Fernet(encrypt_code)
            enc_password = fernet.encrypt(bytes(self.ui.password_box.text(), 'UTF-8'))
            for index in range(self.ui.nicknames_combo.count()):
                if index < (self.ui.nicknames_combo.count() - 1):
                    nicknames_list.append(self.ui.nicknames_combo.itemText(self.ui.nicknames_combo.count()))
            if self.ui.encoding_combo.currentText() == 'DOS (866)':
                profiles[str(self.ui.profname_box.text())] = {'AuthMethod': self.ui.authmethod_combo.currentText(), 'Nicknames': profiles[str(self.ui.profname_box.text())]['Nicknames'], 'Server': self.ui.server_box.text(), 'Port': str(self.ui.port_box.value()), 'Password': enc_password.decode('UTF-8'), 'EncryptCode': encrypt_code.decode('UTF-8'), 'Encoding': 'cp866', 'QuitingMsg': self.ui.quiting_msg_box.text()}
            elif self.ui.encoding_combo.currentText() == 'KOI8-R':
                profiles[str(self.ui.profname_box.text())] = {'AuthMethod': self.ui.authmethod_combo.currentText(), 'Nicknames': profiles[str(self.ui.profname_box.text())]['Nicknames'], 'Server': self.ui.server_box.text(), 'Port': str(self.ui.port_box.value()), 'Password': enc_password.decode('UTF-8'), 'EncryptCode': encrypt_code.decode('UTF-8'), 'Encoding': 'koi8_r', 'QuitingMsg': self.ui.quiting_msg_box.text()}
            elif self.ui.encoding_combo.currentText() == 'KOI8-U':
                profiles[str(self.ui.profname_box.text())] = {'AuthMethod': self.ui.authmethod_combo.currentText(), 'Nicknames': profiles[str(self.ui.profname_box.text())]['Nicknames'], 'Server': self.ui.server_box.text(), 'Port': str(self.ui.port_box.value()), 'Password': enc_password.decode('UTF-8'), 'EncryptCode': encrypt_code.decode('UTF-8'), 'Encoding': 'koi8_u', 'QuitingMsg': self.ui.quiting_msg_box.text()}
            else:
                profiles[str(self.ui.profname_box.text())] = {'AuthMethod': self.ui.authmethod_combo.currentText(), 'Nicknames': profiles[str(self.ui.profname_box.text())]['Nicknames'], 'Server': self.ui.server_box.text(), 'Port': str(self.ui.port_box.value()), 'Password': enc_password.decode('UTF-8'), 'EncryptCode': encrypt_code.decode('UTF-8'), 'Encoding': self.ui.encoding_combo.currentText(), 'QuitingMsg': self.ui.quiting_msg_box.text()}
            with open('profiles', 'w') as configfile:
                profiles.write(configfile)
        except Exception as e:
                pass

    def clear_nicknames(self):
        self.ui.nicknames_combo.currentIndexChanged.disconnect()
        self.ui.nicknames_combo.clear()
        self.ui.nicknames_combo.addItem('')
        settings.read('settings')
        try:
            profiles[str(self.ui.profname_box.text())]['Nicknames'] = ''
            with open('profiles', 'w') as configfile:
                profiles.write(configfile)
        except Exception as e:
                print(e)
        if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
            self.ui.nicknames_combo.addItem(ru_RU.get()['makenick'])
        elif settings.sections() != [] and settings['Main']['Language'] == 'English':
            self.ui.nicknames_combo.addItem(en_US.get()['makenick'])
        self.ui.clear_nicknames_btn.setEnabled(False)
        self.ui.clear_nicknames_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
        self.timer.start(200)

class SettingsWizard002(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = swiz_002()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.show_custom_edit_dlg)
        self.ui.profname.setVisible(False)

    def show_custom_edit_dlg(self):
        settings.read('settings')
        profiles.read('profiles')
        if self.ui.label.text() == en_US.get()['chprofnm'] or self.ui.label.text() == ru_RU.get()['chprofnm']:
            if profiles.sections() == [] or search(profiles.sections(), self.ui.lineEdit.text()) == False:
                profiles[str(self.ui.lineEdit.text())] = {'AuthMethod': '', 'Nicknames': '', 'Server': '', 'Port': '', 'Encoding': '', 'QuitingMsg': 'Tinelix IRC Client ver. {0} ({1})'.format(version, date)}
                with open('profiles', 'w') as configfile:
                    profiles.write(configfile)
            swiz003 = SettingsWizard003()
            swiz003.ui.title_label.setText(str(self.ui.lineEdit.text()))
            swiz003.ui.profname_box.setText(str(self.ui.lineEdit.text()))
            try:
                if profiles.sections() != [] or profiles[str(self.ui.lineEdit.text())]['Nicknames'] != "" and profiles[str(self.ui.lineEdit.text())]['Nicknames'] != " " and profiles[str(self.ui.lineEdit.text())]['Nicknames'] != None:
                    for nick in list(profiles[str(self.ui.lineEdit.text())]['Nicknames'].split(", ")):
                        if nick != "" and nick != " ":
                            swiz003.ui.nicknames_combo.addItem(nick)
                    swiz003.ui.server_box.setText(profiles[str(self.ui.lineEdit.text())]['Server'])
                    swiz003.ui.port_box.setValue(int(profiles[str(self.ui.lineEdit.text())]['Port']))
                    swiz003.ui.quiting_msg_box.setText(profiles[str(self.ui.lineEdit.text())]['quitingmsg'])
                else:
                    swiz003.ui.nicknames_combo.addItem('')
                    swiz003.ui.clear_nicknames_btn.setEnabled(False)
                    swiz003.ui.clear_nicknames_btn.setStyleSheet('color: #4f4f4f')
            except Exception as e:
                if swiz003.ui.nicknames_combo.count() == 0:
                    swiz003.ui.nicknames_combo.addItem('')
            if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                swiz003.ui.nicknames_combo.addItem(ru_RU.get()['makenick'])
            elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                swiz003.ui.nicknames_combo.addItem(en_US.get()['makenick'])
            if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                swiz003.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            elif settings.sections() != [] and settings['Main']['DarkTheme'] == 'Enabled':
                swiz003.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            swiz003.ui.encoding_combo.addItem('UTF-8')
            swiz003.ui.encoding_combo.addItem('Windows-1251')
            swiz003.ui.encoding_combo.addItem('DOS (866)')
            swiz003.ui.encoding_combo.addItem('KOI8-R')
            swiz003.ui.encoding_combo.addItem('KOI8-U')
            swiz003.ui.authmethod_combo.addItem('NickServ')
            if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                swiz003.ui.authmethod_combo.addItem(ru_RU.get()['w_o_auth'])
            elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                swiz003.ui.authmethod_combo.addItem(en_US.get()['w_o_auth'])
            try:
                swiz003.ui.quiting_msg_box.setText(profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['quitingmsg'])
            except:
                swiz003.ui.quiting_msg_box.setText('Tinelix IRC Client (codename Flight, {0}, {1})'.format(version, date))
            try:
                fernet = Fernet(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['EncryptCode'].encode('UTF-8'))
                self.password = fernet.decrypt(bytes(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Password'], 'UTF-8')).decode(self.encoding)
                swiz003.ui.password_box.setText(self.password)
            except:
                pass
            try:
                swiz003.ui.encoding_combo.setCurrentText(profiles[str(self.ui.lineEdit.text())]['encoding'])
            except Exception as e:
                pass
            translator.translate_003(self, swiz003.ui, settings['Main']['Language'], en_US, ru_RU)
            swiz003.exec_()
        elif self.ui.label.text() == en_US.get()['chnicknm'] or self.ui.label.text() == ru_RU.get()['chnicknm']:
            swiz003 = SettingsWizard003()
            profiles.read('profiles')
            swiz003.ui.profname_box.setText(str(self.ui.profname.text()))
            try:
                if profiles[str(self.ui.profname.text())]['Nicknames'] != "" and profiles[str(self.ui.profname.text())]['Nicknames'] != " ":
                    profiles[str(self.ui.profname.text())]['Nicknames'] = profiles[str(self.ui.profname.text())]['Nicknames'] + ', ' + self.ui.lineEdit.text()
                    with open('profiles', 'w') as configfile:
                        profiles.write(configfile)
                else:
                     profiles[str(self.ui.profname.text())]['Nicknames'] = self.ui.lineEdit.text()
                     with open('profiles', 'w') as configfile:
                        profiles.write(configfile)
                for nick in list(profiles[str(self.ui.profname.text())]['Nicknames'].split(", ")):
                    if nick != "" and nick != " ":
                        swiz003.ui.nicknames_combo.addItem(nick)
                swiz003.ui.server_box.setText(profiles[str(self.ui.profname.text())]['Server'])
                swiz003.ui.port_box.setValue(int(profiles[str(self.ui.profname.text())]['Port']))
                swiz003.ui.quiting_msg_box.setText(profiles[str(self.ui.profname.text())]['quitingmsg'])
            except Exception as e:
                if swiz003.ui.nicknames_combo.count() == 0:
                    swiz003.ui.nicknames_combo.addItem('')
            swiz003.ui.title_label.setText(str(self.ui.profname.text()))
            if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                swiz003.ui.nicknames_combo.addItem(ru_RU.get()['makenick'])
            elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                swiz003.ui.nicknames_combo.addItem(en_US.get()['makenick'])
            if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                swiz003.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            elif settings.sections() != [] and settings['Main']['DarkTheme'] == 'Enabled':
                swiz003.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            swiz003.ui.encoding_combo.addItem('UTF-8')
            swiz003.ui.encoding_combo.addItem('Windows-1251')
            swiz003.ui.encoding_combo.addItem('DOS (866)')
            swiz003.ui.encoding_combo.addItem('KOI8-R')
            swiz003.ui.encoding_combo.addItem('KOI8-U')
            swiz003.ui.authmethod_combo.addItem('NickServ')
            swiz003.ui.authmethod_combo.addItem('Без аутентификации')
            try:
                swiz003.ui.encoding_combo.setCurrentText(profiles[str(self.ui.profname.text())]['encoding'])
                swiz003.ui.quiting_msg_box.setText(profiles[str(self.ui.profname.text())]['quitingmsg'])
            except:
                pass
            translator.translate_003(self, swiz003.ui, settings['Main']['Language'], en_US, ru_RU)
            swiz003.exec_()

class SettingsWizard001(QtWidgets.QDialog, swiz_001):
    def __init__(self, parent=None):
        super(SettingsWizard001, self).__init__(parent)
        self.ui = swiz_001()
        self.ui.setupUi(self)
        self.ui.language_combo.addItem('Russian')
        self.ui.language_combo.addItem('English')
        self.ui.add_profile_btn.clicked.connect(self.show_custom_edit_dlg)
        self.ui.connect_btn.clicked.connect(self.irc_connect)
        self.ui.change_profile_btn.clicked.connect(self.edit_item)
        self.ui.del_profile_btn.clicked.connect(self.del_item)
        settings.read('settings')
        profiles.read('profiles')
        self.ui.tableWidget.setRowCount(1);
        self.ui.tableWidget.setColumnCount(2);
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.itemClicked.connect(self.click_item)
        self.ui.tableWidget.itemDoubleClicked.connect(self.edit_item)
        self.ui.connect_btn.setEnabled(False)
        self.ui.connect_btn.setStyleSheet('color: #4f4f4f')
        self.ui.change_profile_btn.setEnabled(False)
        self.ui.change_profile_btn.setStyleSheet('color: #4f4f4f')
        self.ui.del_profile_btn.setEnabled(False)
        self.ui.del_profile_btn.setStyleSheet('color: #4f4f4f')
        self.parent = parent
        self.channel = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(100)
        self.sections_count = None
        try:
            if settings['Main']['DarkTheme'] == 'Disabled':
                self.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            else:
                self.setStyleSheet('background-color: #313131\ncolor: #ffffff;')
        except:
            pass
        if (profiles.sections() != [] or profiles.sections() != None):
            self.ui.tableWidget.setRowCount(0)
            sections_list = []
            for section in profiles.sections():
                sections_list.append(str(section))
            self.sections_count = len(sections_list)
            for section in sections_list:
                rowPosition = sections_list.index(section)
                self.ui.tableWidget.insertRow(rowPosition)
                self.ui.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(section))
                if profiles[section]['Server'] != '':
                    self.ui.tableWidget.setItem(rowPosition, 1, QTableWidgetItem('{0}:{1}'.format(profiles[section]['Server'], profiles[section]['Port'])))
                else:
                    self.ui.tableWidget.setItem(rowPosition, 1, QTableWidgetItem('-'))

    def tick(self):
        sections_list = []
        for section in profiles.sections():
            sections_list.append(str(section))
        if self.sections_count != len(sections_list):
            self.ui.tableWidget.setRowCount(0)

            for section in sections_list:
                rowPosition = sections_list.index(section)
                self.ui.tableWidget.insertRow(rowPosition)
                self.ui.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(section))
                if profiles[section]['Server'] != '':
                    self.ui.tableWidget.setItem(rowPosition, 1, QTableWidgetItem('{0}:{1}'.format(profiles[section]['Server'], profiles[section]['Port'])))
                else:
                    self.ui.tableWidget.setItem(rowPosition, 1, QTableWidgetItem('-'))
            self.sections_count = len(sections_list)

    def show_custom_edit_dlg(self):
        swiz002 = SettingsWizard002()
        settings.read('settings')
        if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
            swiz002.ui.label.setText(ru_RU.get()['chprofnm'])
        elif settings.sections() != [] and settings['Main']['Language'] == 'English':
            swiz002.ui.label.setText(en_US.get()['chprofnm'])
        if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
            swiz002.setStyleSheet('background-color: #ffffff; color: #000000;')
        elif settings.sections() != [] and settings['Main']['DarkTheme'] == 'Enabled':
            swiz002.setStyleSheet('background-color: #313131; color: #ffffff;')
        swiz002.exec_()

    def irc_connect(self):
        self.thread = Thread(self)
        self.thread.started.connect(self.started)
        self.thread.start()
        self.now = datetime.datetime.now()
        self.parent.ui.message_text.setText('')
        self.parent.ui.message_text.setEnabled(True)
        if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
            self.parent.ui.message_text.setStyleSheet('selection-background-color: rgb(255, 119, 0); color: #000000')
        else:
            self.parent.ui.message_text.setStyleSheet('selection-background-color: rgb(161, 75, 0); color: #ffffff')
        if self.parent.ui.message_text.text() != '':
            self.parent.ui.send_msg_btn.setEnabled(True)
            if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                self.parent.ui.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
            else:
               self.parent.ui.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
            self.parent.ui.message_text.returnPressed.connect(self.send_msg)
        else:
            self.parent.ui.send_msg_btn.setEnabled(False)
            self.parent.ui.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
        self.parent.ui.send_msg_btn.clicked.connect(self.send_msg)
        self.parent.ui.message_text.textChanged.connect(self.msgtext_changing)
        settings.read('settings')
        if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
            self.ui.connect_btn.setText(ru_RU.get()['dscn_btn'])
        elif settings.sections() != [] and settings['Main']['Language'] == 'English':
            self.ui.connect_btn.setText(en_US.get()['dscn_btn'])
        self.ui.connect_btn.clicked.disconnect()
        self.ui.connect_btn.clicked.connect(self.irc_disconnect)

    def msgtext_changing(self):
        if self.parent.ui.message_text.text() != '':
            self.parent.ui.send_msg_btn.setEnabled(True)
            self.contextMenu = QMenu(self)
            if self.parent.ui.message_text.text() == '/' and settings.sections() != [] and settings['Main']['MessagesHint'] == 'Enabled':
                settings.read('settings')
                if settings.sections() != [] and settings['Main']['Language'] == 'English':
                    self.signin_item = self.contextMenu.addAction(en_US.get()['nicksv_a'], self.command_choosed)
                    self.joinch_item = self.contextMenu.addAction(en_US.get()['joinch_a'], self.command_choosed)
                    self.names_item = self.contextMenu.addAction(en_US.get()['namesact'], self.command_choosed)
                    self.whois_item = self.contextMenu.addAction(en_US.get()['whois_a'], self.command_choosed)
                    self.part_item = self.contextMenu.addAction(en_US.get()['part_act'], self.command_choosed)
                    self.quit_item = self.contextMenu.addAction(en_US.get()['quit_act'], self.command_choosed)
                    self.hidemenu_item = self.contextMenu.addAction(ru_RU.get()['hidemn_a'])
                else:
                    self.signin_item = self.contextMenu.addAction(ru_RU.get()['nicksv_a'], self.command_choosed)
                    self.joinch_item = self.contextMenu.addAction(ru_RU.get()['joinch_a'], self.command_choosed)
                    self.names_item = self.contextMenu.addAction(ru_RU.get()['namesact'], self.command_choosed)
                    self.whois_item = self.contextMenu.addAction(ru_RU.get()['whois_a'], self.command_choosed)
                    self.part_item = self.contextMenu.addAction(ru_RU.get()['part_act'], self.command_choosed)
                    self.quit_item = self.contextMenu.addAction(ru_RU.get()['quit_act'], self.command_choosed)
                    self.hidemenu_item = self.contextMenu.addAction(ru_RU.get()['hidemn_a'])
                try:
                    commands = self.contextMenu.popup(self.parent.ui.message_text.mapToGlobal(QPoint(0, -176)))
                except Exception as e:
                    print(e)
            settings.read('settings')
            if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                self.parent.ui.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
            else:
               self.parent.ui.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
            self.parent.ui.message_text.returnPressed.connect(self.send_msg)
        else:
            self.parent.ui.send_msg_btn.setEnabled(False)
            self.parent.ui.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
            try:
                self.parent.ui.message_text.returnPressed.disconnect()
            except:
                pass
    @QtCore.pyqtSlot()
    def command_choosed(self):
        command = self.sender()
        if command == self.signin_item:
            self.parent.ui.message_text.setText('/nickserv')
        elif command == self.joinch_item:
            self.parent.ui.message_text.setText('/join #')
        elif command == self.names_item:
            self.parent.ui.message_text.setText('/names')
        elif command == self.whois_item:
            self.parent.ui.message_text.setText('/whois')
        elif command == self.part_item:
            self.parent.ui.message_text.setText('/part')
        elif command == self.quit_item:
            self.parent.ui.message_text.setText('/quit')

    def irc_disconnect(self):
        try:
            profiles.read('profiles')
            print('Disconnecting...')
            self.socket.send(bytes('QUIT {0}\r\n'.format(profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['quitingmsg']), self.encoding))
            self.socket.close()
            self.parent.ui.send_msg_btn.setEnabled(False)
            self.parent.ui.message_text.setEnabled(False)
            self.ui.connect_btn.clicked.connect(self.irc_connect)
            settings.read('settings')
            if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                self.ui.connect_btn.setText(ru_RU.get()['conn_btn'])
            elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                self.ui.connect_btn.setText(en_US.get()['conn_btn'])
            self.timer.start()
            self.parent.ui.members_list.clear()
            self.parent.ui.members_list.setVisible(False)
            self.parent.ui.conn_quality_progr.setValue(0)
            self.parent.ui.latency_label.setText('')
            self.parent.ui.message_text.setEnabled(False)
        except Exception as e:
            print(e)

    @QtCore.pyqtSlot(str, str, float, str, str, str, float, socket.socket)
    def started(self, status, server, port, nickname, encoding, quiting_msg, ping, socket):
        self.socket = socket
        self.encoding = encoding
        self.server = server
        self.port = port
        self.nickname = nickname
        self.quiting_msg = quiting_msg
        self.members = []
        self.operators = []
        self.owners = []
        self.parent.setWindowTitle('Tinelix IRC Client | {0}'.format(self.server))
        settings.read('settings')
        text = '{}'.format(status)
        msg_list = status.splitlines()
        for msg_line in msg_list:
            if msg_line.startswith('PING'):
                self.ping = time.time()
            elif msg_line.startswith('PONG'):
                self.last_ping = time.time()
                try:
                    if round((self.last_ping - self.ping) * 1000, 2) > 0.9:
                        self.parent.ui.conn_quality_progr.setValue(round(5000 - ((self.last_ping - self.ping) * 1000)))
                        if round((self.last_ping - self.ping) * 1000, 2) < 1000:
                            self.parent.ui.latency_label.setText('({0} ms)'.format(round((self.last_ping - self.ping) * 1000, 2)))
                        else:
                            self.parent.ui.latency_label.setText('({0} ms)'.format(round((self.last_ping - self.ping) * 1000, 1)))
                        self.parent.ui.status_label.setText(ru_RU.get()['rdstatus'])
                    else:
                       self.parent.ui.conn_quality_progr.setValue(0)
                       self.parent.ui.latency_label.setText('')
                except:
                    pass
            elif msg_line.startswith('{0} {1}'.format(self.server, 353)):
                try:
                    self.names_raw = msg_line.split(' ')[5:]
                    for nick in self.names_raw:
                        if nick.startswith('@'):
                            self.operators.append(nick.replace(':', '').replace('&', '').replace('@', ''))
                        elif nick.startswith('~'):
                            self.owners.append(nick.replace(':', '').replace('~', '').replace('&', '').replace('@', ''))
                        else:
                            self.members.append(nick.replace(':', '').replace('~', '').replace('&', ''))
                except Exception as e:
                    print(e)
            elif msg_line.startswith('{0} {1}'.format(self.server, 366)):
                self.parent.ui.members_list.clear()
                if settings['Main']['Language'] == 'English':
                    owners_list = QTreeWidgetItem([en_US.get()['owners']])
                    operators_list = QTreeWidgetItem([en_US.get()['oprtors']])
                    members_list = QTreeWidgetItem([en_US.get()['members']])
                else:
                    owners_list = QTreeWidgetItem([ru_RU.get()['owners']])
                    operators_list = QTreeWidgetItem([ru_RU.get()['oprtors']])
                    members_list = QTreeWidgetItem([ru_RU.get()['members']])
                for operator in self.operators:
                    if operator != '':
                        child = QTreeWidgetItem([operator])
                        operators_list.addChild(child)
                for member in self.members:
                    if member != '':
                        child = QTreeWidgetItem([member])
                        members_list.addChild(child)
                for owner in self.owners:
                    if owner != '':
                        child = QTreeWidgetItem([owner])
                        owners_list.addChild(child)
                self.parent.ui.members_list.addTopLevelItems([owners_list, operators_list, members_list])
                operators_list.setExpanded(True)
                members_list.setExpanded(True)
                owners_list.setExpanded(True)
                self.parent.ui.members_list.setVisible(True)

            elif msg_line.find('PRIVMSG') != -1:
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[2] == 'PRIVMSG':
                        self.parent.ui.chat_text.setPlainText('{0}\n{1}: {2} ({3})'.format(self.parent.ui.chat_text.toPlainText(), decoded_text[0], ' '.join(decoded_text[4:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        self.parent.ui.chat_text.moveCursor(QTextCursor.End)
                except Exception as e:
                    print(e)
                    self.parent.ui.chat_text.setPlainText('{0}\n{1}'.format(self.parent.ui.chat_text.toPlainText(), msg_line))
                    self.parent.ui.chat_text.moveCursor(QTextCursor.End)
            elif msg_line.find('JOIN') != -1:
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[2] == 'JOIN':
                        self.parent.ui.chat_text.setPlainText('{0}\n{1} joined on the channel {2}. ({3})'.format(self.parent.ui.chat_text.toPlainText(), decoded_text[0], " ".join(decoded_text[3:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        self.parent.ui.chat_text.moveCursor(QTextCursor.End)
                        try:
                            if settings['Main']['Language'] == 'English':
                                self.parent.ui.status_label.setText(en_US.get()['chstatus'].format(''.join(decoded_text[3].splitlines()[0])))
                            else:
                                self.parent.ui.status_label.setText(ru_RU.get()['chstatus'].format(''.join(decoded_text[3].splitlines()[0])))
                        except:
                            pass
                        self.socket.send(bytes('NAMES {0}\r\n'.format(self.parent.ui.channel_name.text()), self.encoding))
                except Exception as e:
                    print(e)
                    self.parent.ui.chat_text.setPlainText('{0}\n{1}'.format(self.parent.ui.chat_text.toPlainText(), msg_line))
                    self.parent.ui.chat_text.moveCursor(QTextCursor.End)
            elif msg_line.find('QUIT') != -1:
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[2] == 'QUIT':
                        self.parent.ui.chat_text.setPlainText('{0}\n{1} quited with reason: {2}. ({3})'.format(self.parent.ui.chat_text.toPlainText(), decoded_text[0], " ".join(decoded_text[3:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        self.parent.ui.chat_text.moveCursor(QTextCursor.End)
                        if settings['Main']['Language'] == 'English':
                            self.parent.ui.status_label.setText(en_US.get()['rdstatus'])
                        else:
                            self.parent.ui.status_label.setText(ru_RU.get()['rdstatus'])
                        self.socket.send(bytes('NAMES {0}\r\n'.format(self.parent.ui.channel_name.text()), self.encoding))
                except:
                    self.parent.ui.chat_text.setPlainText('{0}\n{1}'.format(self.parent.ui.chat_text.toPlainText(), msg_line))
                    self.parent.ui.chat_text.moveCursor(QTextCursor.End)
            elif msg_line.find('NICK') != -1:
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[2] == 'NICK':
                        self.parent.ui.chat_text.setPlainText('{0}\n{1} changed nickname to {2}. ({3})'.format(self.parent.ui.chat_text.toPlainText(), decoded_text[0], " ".join(decoded_text[3:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        self.parent.ui.chat_text.moveCursor(QTextCursor.End)
                        if settings['Main']['Language'] == 'English':
                            self.parent.ui.status_label.setText(en_US.get()['rdstatus'])
                        else:
                            self.parent.ui.status_label.setText(ru_RU.get()['rdstatus'])
                except:
                    self.parent.ui.chat_text.setPlainText('{0}\n{1}'.format(self.parent.ui.chat_text.toPlainText(), msg_line))
                    self.parent.ui.chat_text.moveCursor(QTextCursor.End)
            elif msg_line.startswith('Exception: '):
                self.parent.ui.chat_text.setPlainText('{0}'.format(msg_line))
            else:
                self.parent.ui.chat_text.setPlainText('{0}\n{1}'.format(self.parent.ui.chat_text.toPlainText(), msg_line))
                self.parent.ui.chat_text.moveCursor(QTextCursor.End)
            if not msg_line.startswith('Exception: ') and settings.sections() != [] and settings['Main']['MsgHistory'] == 'Enabled':
                if not os.path.exists('history'):
                    os.makedirs('history')
                    with open('history/irc_{0}_{1}.txt'.format(str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()), self.now.strftime('%Y-%m-%d_%H.%M.%S')), 'w+') as f:
                        f.write(self.parent.ui.chat_text.toPlainText())
                else:
                    with open('history/irc_{0}_{1}.txt'.format(str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()), self.now.strftime('%Y-%m-%d_%H.%M.%S')), 'w+') as f:
                        f.write(self.parent.ui.chat_text.toPlainText())

    def send_msg(self):
        if self.parent.ui.message_text.text().startswith('/join #'):
            msg_list = self.parent.ui.message_text.text().split(' ')
            self.channel = msg_list[1]
            try:
                self.socket.send(bytes('JOIN {0}\r\n'.format(msg_list[1]), self.encoding))
                self.parent.ui.channel_name.setText(msg_list[1])
            except:
                pass
        elif self.parent.ui.message_text.text().startswith('/whois '):
            try:
                msg_list = self.parent.ui.message_text.text().split(' ')
                nick = msg_list[1]
                self.socket.send(bytes('WHOIS {0}\r\n'.format(msg_list[1]), self.encoding))
            except:
                pass
        elif self.parent.ui.message_text.text() == ('/leave') or self.parent.ui.message_text.text() == ('/part'):
            try:
                msg_list = self.parent.ui.message_text.text().split(' ')
                self.socket.send(bytes('PART {0}\r\n'.format(self.channel), self.encoding))
                self.parent.ui.members_list.clear()
                self.parent.ui.members_list.setVisible(False)
                self.parent.ui.status_label.setText(ru_RU.get()['rdstatus'])
            except:
                pass
        elif self.parent.ui.message_text.text().startswith('/names') or self.parent.ui.message_text.text().startswith('/members'):
            try:
                msg_list = self.parent.ui.message_text.text().split(' ')
                self.socket.send(bytes('NAMES {0}\r\n'.format(msg_list[1]), self.encoding))
            except:
                self.socket.send(bytes('NAMES {0}\r\n'.format(self.channel), self.encoding))
        elif self.parent.ui.message_text.text().startswith('/nickserv identify') or self.parent.ui.message_text.text().startswith('/msg nickserv identify'):
            msg_list = self.parent.ui.message_text.text().split(' ')
            password = msg_list[len(msg_list) - 1]
            self.socket.send(bytes('PRIVMSG nickserv identify {0} {1}\r\n'.format(self.nickname, password), self.encoding))
        elif self.parent.ui.message_text.text() == '/info':
            try:
                self.socket.send(bytes('INFO\r\n', self.encoding))
            except:
                pass
        elif self.parent.ui.message_text.text() == '/disconnect' or self.parent.ui.message_text.text().startswith('/quit'):
            settings.read('settings')
            self.socket.send(bytes('QUIT {0}\r\n'.format(self.quiting_msg), self.encoding))
            self.socket.close()
            self.ui.connect_btn.clicked.connect(self.irc_connect)
            if settings.sections() != [] and settings['Main']['Language'] == 'English':
                self.ui.connect_btn.setText(en_US.get()['conn_btn'])
            else:
                self.ui.connect_btn.setText(ru_RU.get()['conn_btn'])
            self.parent.ui.members_list.clear()
            self.parent.ui.members_list.setVisible(False)
            self.parent.setWindowTitle('Tinelix IRC Client')
            if settings.sections() != [] and settings['Main']['Language'] == 'English':
                self.parent.ui.message_text.setText(en_US.get()['cantsmsg'])
            else:
                self.parent.ui.message_text.setText(ru_RU.get()['cantsmsg'])
            self.parent.ui.conn_quality_progr.setValue(0)
            self.parent.ui.latency_label.setText('')
            self.parent.ui.message_text.setEnabled(False)
        elif self.channel != None:
            self.socket.send(bytes('PRIVMSG {0} :{1}\r\n'.format(self.channel, self.parent.ui.message_text.text()), self.encoding))
        if self.parent.ui.message_text.text().startswith('/nickserv identify'):
            self.parent.ui.chat_text.setPlainText('{0}\n{1}: {2} [password] ({3})'.format(self.parent.ui.chat_text.toPlainText(), self.nickname, ' '.join(self.parent.ui.message_text.text().split(' ')[:2]), datetime.datetime.now().strftime("%H:%M:%S")))
        else:
            self.parent.ui.chat_text.setPlainText('{0}\n{1}: {2} ({3})'.format(self.parent.ui.chat_text.toPlainText(), self.nickname, self.parent.ui.message_text.text(), datetime.datetime.now().strftime("%H:%M:%S")))
        self.parent.ui.message_text.setText('')
        self.parent.ui.chat_text.moveCursor(QTextCursor.End)

    def edit_item(self):
        swiz003 = SettingsWizard003()
        swiz003.ui.title_label.setText(str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()))
        swiz003.ui.profname_box.setText(str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()))
        profiles.read('profiles')
        settings.read('settings')
        try:
            if profiles.sections() != [] and profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['Nicknames'] != "" and profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['Nicknames'] != " " and profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['Nicknames'] != None:
                for nick in list(profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['Nicknames'].split(", ")):
                    if nick != "" and nick != " ":
                        swiz003.ui.nicknames_combo.addItem(nick)
                swiz003.ui.server_box.setText(profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['Server'])
                swiz003.ui.port_box.setValue(int(profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['Port']))
                if profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['quitingmsg'] == '' and profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['quitingmsg'] == None:
                    swiz003.ui.quiting_msg_box.setText('Tinelix IRC Client (codename Flight, {0}, {1})'.format(version, date))
                else:
                    swiz003.ui.quiting_msg_box.setText(profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['quitingmsg'])
            else:
                swiz003.ui.nicknames_combo.addItem('')
                swiz003.ui.clear_nicknames_btn.setEnabled(False)
                swiz003.ui.clear_nicknames_btn.setStyleSheet('color: #4f4f4f')
        except Exception as e:
            if swiz003.ui.nicknames_combo.count() == 0:
                swiz003.ui.nicknames_combo.addItem('')
        if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
            swiz003.ui.nicknames_combo.addItem(ru_RU.get()['makenick'])
        elif settings.sections() != [] and settings['Main']['Language'] == 'English':
            swiz003.ui.nicknames_combo.addItem(en_US.get()['makenick'])
        if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
            swiz003.setStyleSheet('background-color: #ffffff; color: #000000;')
        elif settings.sections() != [] and settings['Main']['DarkTheme'] == 'Enabled':
            swiz003.setStyleSheet('background-color: #313131; color: #ffffff;')
        swiz003.ui.encoding_combo.addItem('UTF-8')
        swiz003.ui.encoding_combo.addItem('Windows-1251')
        swiz003.ui.encoding_combo.addItem('DOS (866)')
        swiz003.ui.encoding_combo.addItem('KOI8-R')
        swiz003.ui.encoding_combo.addItem('KOI8-U')
        swiz003.ui.authmethod_combo.addItem('NickServ')
        swiz003.ui.authmethod_combo.addItem('Без аутентификации')
        try:
            fernet = Fernet(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['EncryptCode'].encode('UTF-8'))
            self.password = fernet.decrypt(bytes(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Password'], 'UTF-8')).decode(self.encoding)
            swiz003.ui.password_box.setText(self.password)
        except:
            pass

        try:
            swiz003.ui.server_box.setText(fernet.decrypt(bytes(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Password'], 'UTF-8')))
        except:
            pass
        try:
            swiz003.ui.encoding_combo.setCurrentText(profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['encoding'])
            self.timer.start()
        except Exception as e:
            print(e)
        translator.translate_003(self, swiz003.ui, settings['Main']['Language'], en_US, ru_RU)
        swiz003.exec_()

    def del_item(self):
        try:
            profiles.remove_section(str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()))
            with open('profiles', 'w') as configfile:
                profiles.write(configfile)
        except Exception as e:
            print(e)
        self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow())
        if self.ui.tableWidget.rowCount() == 0:
            self.ui.tableWidget.itemDoubleClicked.connect(self.edit_item)
            self.ui.connect_btn.setEnabled(False)
            self.ui.connect_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
            self.ui.change_profile_btn.setEnabled(False)
            self.ui.change_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
            self.ui.del_profile_btn.setEnabled(False)
            self.ui.del_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
            self.timer.start()

    def click_item(self):
        profiles.read('profiles')
        settings.read('settings')
        self.ui.change_profile_btn.setEnabled(True)
        if settings['Main']['DarkTheme'] == 'Disabled':
            self.ui.change_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
        else:
            self.ui.change_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
        self.ui.del_profile_btn.setEnabled(True)
        if settings['Main']['DarkTheme'] == 'Disabled':
            self.ui.del_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
        else:
            self.ui.del_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
        try:
            if profiles[self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()]['server'] != '' and profiles[self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()]['port'] != '':
                self.ui.connect_btn.setEnabled(True)
                if settings['Main']['DarkTheme'] == 'Disabled':
                    self.ui.connect_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
                else:
                    self.ui.connect_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
            self.timer.stop()
        except:
            pass

class AboutProgramDlg(QtWidgets.QDialog, swiz_001):
    def __init__(self, parent=None):
        super(AboutProgramDlg, self).__init__(parent)
        self.ui = aboutprg()
        self.ui.setupUi(self)
        self.parent = parent
        settings.read('settings')
        self.ui.repo_btn.clicked.connect(self.repo_open)

    def repo_open(self):
        webbrowser.open('https://github.com/tinelix/irc-client')

class AdvancedSettingsDlg(QtWidgets.QDialog, ext_sett):
    def __init__(self, parent=None):
        super(AdvancedSettingsDlg, self).__init__(parent)
        self.ui = ext_sett()
        self.ui.setupUi(self)
        self.parent = parent
        settings.read('settings')

app = QtWidgets.QApplication([])
app.setStyle('Fusion')
application = mainform()
application.show()

sys.exit(app.exec())
