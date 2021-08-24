#!/usr/bin/python3
import sys, PyQt5, dlg001, configparser, time, threading, socket, translator, webbrowser, os, base64
import languages.ru_RU as ru_RU
import languages.en_US as en_US
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

settings = configparser.ConfigParser()
profiles = configparser.ConfigParser()

version = '0.1 Beta'
date = '2021-08-24'

enckey = Fernet.generate_key()
fernet = Fernet(enckey)

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

class Thread(QThread):
    logged = QtCore.pyqtSignal(str, str, int, str, str, str, int, socket.socket)
    started = QtCore.pyqtSignal(str, str, int, str, str, str, int, socket.socket)

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
        self.ui.about_item.triggered.connect(self.about_window)
        self.ui.connect_item.triggered.connect(self.connect_window)
        self.ui.quit_item.triggered.connect(self.quit_app)
        self.ui.conn_quality_progr.setValue(0)
        self.ui.latency_label.setText("")
        self.child = SettingsWizard001(self)
        self.child_2 = SettingsWizard002()
        self.child_3 = SettingsWizard003()
        self.child_4 = AboutProgramDlg()
        settings.read('settings')
        profiles.read('profiles')
        print('Tinelix codename Flight {0} ({1})\nDone!'.format(version, date))
        self.ui.dialogs_list.setVisible(False)
        self.ui.members_list.setVisible(False)

        if settings.sections() == []:
            settings['Main'] = {'Language': 'Russian', 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled'}
            with open('settings', 'w') as configfile:
                settings.write(configfile)
        else:
            translator.translate_001(self, self.child.ui, settings['Main']['Language'], en_US, ru_RU)

        #swiz001 = SettingsWizard001()
        self.child.show()
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

    def about_window(self):
        settings.read('settings')
        self.version = version
        if settings.sections() == []:
            settings['Main'] = {'Language': 'Russian', 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled'}
            with open('settings', 'w') as configfile:
                settings.write(configfile)
            translator.translate_004(self, self.child_4.ui, 'Russian', en_US, ru_RU)
        else:
            translator.translate_004(self, self.child_4.ui, settings['Main']['Language'], en_US, ru_RU)
        self.child_4.exec_()

    def connect_window(self):
        self.child.ui.language_label.setVisible(False)
        self.child.ui.language_combo.setVisible(False)
        self.child.exec_()

    def quit_app(self):
        print('Quiting...')
        self.close()

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
        self.timer.start(200)

    def tick(self):
        self.ui.nicknames_combo.currentIndexChanged.connect(self.show_create_nickname_dlg)
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
                profiles[str(self.ui.lineEdit.text())] = {'AuthMethod': '', 'Nicknames': '', 'Server': '', 'Port': '', 'Encoding': '', 'QuitingMsg': ''}
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
            swiz003.ui.encoding_combo.addItem('UTF-8')
            swiz003.ui.encoding_combo.addItem('Windows-1251')
            swiz003.ui.encoding_combo.addItem('DOS (866)')
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
            swiz003.ui.encoding_combo.addItem('UTF-8')
            swiz003.ui.encoding_combo.addItem('Windows-1251')
            swiz003.ui.encoding_combo.addItem('DOS (866)')
            swiz003.ui.authmethod_combo.addItem('NickServ')
            swiz003.ui.authmethod_combo.addItem('Без аутентификации')
            try:
                swiz003.ui.encoding_combo.setCurrentText(profiles[str(self.ui.profname.text())]['encoding'])
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
        swiz002.exec_()

    def irc_connect(self):
        self.thread = Thread(self)
        self.thread.started.connect(self.started)
        self.thread.start()
        self.parent.ui.message_text.setText('')
        self.parent.ui.message_text.setEnabled(True)
        self.parent.ui.message_text.setStyleSheet('selection-background-color: rgb(161, 75, 0); color: #ffffff')
        self.parent.ui.send_msg_btn.setEnabled(True)
        self.parent.ui.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
        self.parent.ui.send_msg_btn.clicked.connect(self.send_msg)
        self.parent.ui.message_text.returnPressed.connect(self.send_msg)
        settings.read('settings')
        if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
            self.ui.connect_btn.setText(ru_RU.get()['dscn_btn'])
        elif settings.sections() != [] and settings['Main']['Language'] == 'English':
            self.ui.connect_btn.setText(en_US.get()['dscn_btn'])
        self.ui.connect_btn.clicked.disconnect()
        self.ui.connect_btn.clicked.connect(self.irc_disconnect)


    def irc_disconnect(self):
        try:
            profiles.read('profiles')
            print('Disconnecting...')
            self.socket.send(bytes('QUIT {0}\r\n'.format(profiles[section]['Server']['quitingmsg']), self.encoding))
            self.socket.close()
            self.ui.connect_btn.clicked.connect(self.irc_connect)
            settings.read('settings')
            if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                self.ui.connect_btn.setText(ru_RU.get()['conn_btn'])
            elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                self.ui.connect_btn.setText(en_US.get()['conn_btn'])
            self.timer.start()
        except Exception as e:
            print(e)

    @QtCore.pyqtSlot(str, str, int, str, str, str, int, socket.socket)
    def started(self, status, server, port, nickname, encoding, quiting_msg, ping, socket):
        self.socket = socket
        self.encoding = encoding
        self.server = server
        self.port = port
        self.nickname = nickname
        self.quiting_msg = quiting_msg
        self.ping = ping
        text = '{}'.format(status)
        msg_list = status.splitlines()
        for msg_line in msg_list:
            if msg_line.startswith('PING '):
                self.last_ping = time.time()
                try:
                    self.parent.ui.conn_quality_progr.setValue(5000 - ((self.last_ping - self.ping) * 1000))
                    self.parent.ui.latency_label.setText('({0} ms)'.format(round((self.last_ping - self.ping) * 1000, 2)))
                except:
                    pass
            elif msg_line.startswith('Exception: '):
                self.parent.ui.chat_text.setPlainText('{0}'.format(msg_line))
            else:
                self.parent.ui.chat_text.setPlainText('{0}\n{1}'.format(self.parent.ui.chat_text.toPlainText(), msg_line))
                self.parent.ui.chat_text.moveCursor(QTextCursor.End)

    def send_msg(self):
        if self.parent.ui.message_text.text().startswith('/join #'):
            msg_list = self.parent.ui.message_text.text().split(' ')
            self.channel = msg_list[1]
            try:
                self.socket.send(bytes('JOIN {0}\r\n'.format(msg_list[1]), self.encoding))
            except:
                pass
        elif self.parent.ui.message_text.text().startswith('/whois '):
            try:
                msg_list = self.parent.ui.message_text.text().split(' ')
                nick = msg_list[1]
                self.socket.send(bytes('WHOIS {0}\r\n'.format(msg_list[1]), self.encoding))
            except:
                pass
        elif self.parent.ui.message_text.text().startswith('/leave') or self.parent.ui.message_text.text().startswith('/part'):
            try:
                msg_list = self.parent.ui.message_text.text().split(' ')
                self.socket.send(bytes('PART {0}\r\n'.format(msg_list[1]), self.encoding))
            except:
                pass
        elif self.parent.ui.message_text.text().startswith('/nickserv identify') or self.parent.ui.message_text.text().startswith('/msg nickserv identify'):
            msg_list = self.parent.ui.message_text.text().split(' ')
            password = msg_list[len(msg_list) - 1]
            self.socket.send(bytes('PRIVMSG nickserv identify {0} {1}\r\n'.format(self.nickname, password), self.encoding))
        elif self.parent.ui.message_text.text() == '/info':
            try:
                self.socket.send(bytes('INFO\r\n', self.encoding))
            except:
                pass
        elif self.parent.ui.message_text.text() == '/disconnect' or self.parent.ui.message_text.text().startswith == '/quit':
            settings.read('settings')
            self.socket.send(bytes('QUIT {0}\r\n'.format(profiles[section]['Server']['quitingmsg']), self.encoding))
            self.socket.close()
        elif self.channel != None:
            self.socket.send(bytes('PRIVMSG {0} :{1}\r\n'.format(self.channel, self.parent.ui.message_text.text()), self.encoding))
        self.parent.ui.chat_text.setPlainText('{0}\n{1}: {2}'.format(self.parent.ui.chat_text.toPlainText(), self.nickname, self.parent.ui.message_text.text()))
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
        swiz003.ui.encoding_combo.addItem('UTF-8')
        swiz003.ui.encoding_combo.addItem('Windows-1251')
        swiz003.ui.encoding_combo.addItem('DOS (866)')
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
        self.ui.change_profile_btn.setEnabled(True)
        self.ui.change_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
        self.ui.del_profile_btn.setEnabled(True)
        self.ui.del_profile_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
        try:
            if profiles[self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()]['server'] != '' and profiles[self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()]['port'] != '':
                self.ui.connect_btn.setEnabled(True)
                self.ui.connect_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
            self.timer.stop()
        except:
            pass

app = QtWidgets.QApplication([])
app.setStyle('Fusion')
application = mainform()
application.show()

sys.exit(app.exec())
