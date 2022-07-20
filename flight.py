#!/usr/bin/python3
import sys, PyQt5, dlg001, configparser, time, threading, socket, translator, webbrowser, os, base64, datetime, traceback, gc,  ssl, tracemalloc, platform
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
import parser
import sconsole
from progresswindow import Ui_Dialog as progrdlg
from chat_widget import Ui_Form as chatwidg
from mention_notif import Ui_Dialog as mention_notif_window

settings = configparser.ConfigParser()
profiles = configparser.ConfigParser()

version = '1.2.0 Stable'
date = '2022-07-20'

init_required = 1

now = datetime.datetime.now()

enckey = Fernet.generate_key()
fernet = Fernet(enckey)

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

class ChatWidget(QtWidgets.QWidget, chatwidg):
    def __init__(self, parent=None):
        super(ChatWidget, self).__init__(parent)
        self.parent = parent
        self = self.setupUi(self)
        try:
            self.chat_text.setObjectName('chat_text_{0}'.format(self.parent.parent.count() + 1))
            self.members_list.setObjectName('members_list_{0}'.format(self.parent.parent.count() + 1))
            self.message_text.setObjectName('message_text_{0}'.format(self.parent.parent.count() + 1))
            self.send_msg_btn.setObjectName('send_msg_btn_{0}'.format(self.parent.parent.count() + 1))
        except:
            pass

class Thread(QThread):
    logged = QtCore.pyqtSignal(str, str, float, str, str, str, float, socket.socket)
    started = QtCore.pyqtSignal(str, str, float, str, str, str, float, socket.socket)
    finished = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.parent = parent
        parent_2 = parent.parent
    def run(self):
            profiles.read('profiles')
            if profiles.sections() != [] or profiles.sections() != None and (profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['server'] != '' and profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['port'] != '') and (profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['nicknames'] != '' and profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['nicknames'] != ''):
                self.ssl = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
                self.encoding = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Encoding']
                self.username = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Nicknames'].split(', ')[0]
                self.server = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Server']
                self.port = int(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Port'])
                self.channel = ""
                self.socket = self.parent.socket
                try:
                    self.socket.settimeout(10)
                except:
                    self.parent.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket = self.parent.socket
                self.quiting_msg = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['quitingmsg']
                try:
                    self.realname = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['realname']
                    self.hostname = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['hostname']
                except:
                    self.realname = self.username
                    self.hostname = self.hostname
                fernet = Fernet(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['EncryptCode'].encode('UTF-8'))
                self.password = fernet.decrypt(bytes(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Password'], 'UTF-8')).decode(self.encoding)
                try:
                    self.until_ping = time.time()
                    threshold = 1 * 60
                    self.ping = time.time()
                    try:
                        if profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['SSL'] == 'Enabled':
                            self.socket = self.ssl.wrap_socket(self.socket)
                    except:
                        pass
                    tracemalloc.start()
                    snapshot = tracemalloc.take_snapshot()
                    self.socket.connect((self.server,self.port))
                    print('Connecting to {0}...'.format(self.server))
                    self.socket.setblocking(True)
                    try:
                        snapshot_2 = tracemalloc.take_snapshot()
                        top_stats = snapshot_2.compare_to(snapshot, 'lineno')
                        for stat in top_stats[:10]:
                            print(stat)
                        if self.hostname == None or self.realname == None or self.hostname == '' or self.realname == '':
                            self.socket.send(bytes("USER " + self.username + " " + self.username + " " + self.username + " :Member\n", self.encoding))
                        else:
                            self.socket.send(bytes("USER " + self.username + " " + self.hostname + " " + self.username + " :" + self.realname + "\n", self.encoding))
                    except:
                        self.socket.send(bytes("USER " + self.username + " " + self.username + " " + self.username + " :Member\n", self.encoding))
                    self.socket.send(bytes("NICK " + self.username + "\n", self.encoding))
                    while True:
                        self.text=self.socket.recv(8192)
                        self.ping = time.time()
                        try:
                            for line in self.text.decode(self.encoding).splitlines():
                                if ' '.join(msg_line.split(' ')[0:2]).find('321') != -1:
                                    self.started.emit('{0}{1}'.format('Please wait...', ':'.join(line.split(":")[2:])), self.server, self.port, self.username, self.encoding, self.quiting_msg, self.ping, self.socket)
                                if ' '.join(msg_line.split(' ')[0:2]).find('322') != -1:
                                    time.sleep(0.2)
                                self.started.emit('{0}{1}'.format(''.join(line.split(":")[:2]), ':'.join(line.split(":")[2:])), self.server, self.port, self.username, self.encoding, self.quiting_msg, self.ping, self.socket)
                        except Exception as e:
                            if not str(e).startswith('\'utf-8\' codec can\'t decode byte'):
                                self.started.emit(''.join(self.text.decode(self.encoding).split(":")), self.server, self.port, self.username, self.encoding, self.quiting_msg, self.ping, self.socket)
                        try:
                            msg_list = self.text.decode(self.encoding).splitlines()
                        except:
                            msg_list = ['Oops']
                        for msg_line in msg_list:
                            if msg_line.startswith('PING'):
                                ping_msg = msg_line.split(' ')
                                self.socket.send(bytes('PONG {0}\r\n'.format(ping_msg[1]), self.encoding))
                                self.started.emit('PONG', self.server, self.port, self.username, self.encoding, self.quiting_msg, self.ping, self.socket)
                            elif msg_line.startswith(':{0} {1}'.format(self.server, '001')) and profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['AuthMethod'] == 'NickServ':
                                self.socket.send(bytes("PRIVMSG nickserv identify {0} {1}\r\n".format(self.username, self.password), self.encoding))
                            elif msg_line.startswith('ERROR'):
                                self.socket.close()
                                tracemalloc.stop()
                            elif msg_line.startswith(':{0} {1}'.format(self.server, 433)):
                                try:
                                    if len(profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Nicknames'].split(', ')) > 1:
                                        self.username = profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Nicknames'].split(', ')[profiles[self.parent.ui.tableWidget.item(self.parent.ui.tableWidget.currentRow(), 0).text()]['Nicknames'].split(', ').index(self.username) + 1]
                                        self.started.emit('We will use the next nickname.', self.server, self.port, self.username, self.encoding, self.quiting_msg, self.ping, self.socket)
                                        self.socket.send(bytes("NICK " + self.username + "\n", self.encoding))
                                except:
                                    pass

                except Exception as e:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    if not str(e).startswith('[Errno 9]'):
                        self.started.emit('Exception: {0}'.format(str(e)), self.server, self.port, self.username, self.encoding, self.quiting_msg, self.ping, self.socket)
                        print("\n".join(ex))
                    self.socket.close()
                    tracemalloc.stop()

    def stop(self):
        self.socket.close()
        self.terminate()

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
        self.child_widget = ChatWidget(self)
        self.ui.about_item.triggered.connect(self.about_window)
        self.ui.connect_item.triggered.connect(self.connect_window)
        self.ui.settings_item.triggered.connect(self.settings_window)
        self.ui.quit_item.triggered.connect(self.quit_app)
        settings.read('settings')
        profiles.read('profiles')
        print('Tinelix codename Flight {0} ({1})\nDone!'.format(version, date))
        if settings.sections() == []:
            settings['Main'] = {'Language': 'Russian', 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'Enabled', 'MessagesHint': 'Disabled', 'MsgBacklight': 'Enabled', 'MsgFont': 'Consolas, 10', 'ParsingDebugger': 'Disabled'}
            with open('settings', 'w') as configfile:
                settings.write(configfile)
            settings.read('settings')
            profiles.read('profiles')
            if settings['Main']['Language'] == 'Russian':
                self.ui.tabs.addTab(self.child_widget, 'Поток')
            else:
               self.ui.tabs.addTab(self.child_widget, 'Thread')
        else:
            if settings['Main']['Language'] == 'Russian':
                self.ui.tabs.addTab(self.child_widget, 'Поток')
            else:
               self.ui.tabs.addTab(self.child_widget, 'Thread')

        self.child_widget.chat_text.setVerticalScrollBar(self.child_widget.verticalScrollBar)
        self.child_widget.members_list.setVerticalScrollBar(self.child_widget.verticalScrollBar_2)
        self.child_widget.members_list.setVisible(False)
        self.child_widget.list_frame.setVisible(False);
        try:
            font = QFont(settings['Main']['MsgFont'].split(', ')[0])
            try:
                font.setPointSize(int(settings['Main']['MsgFont'].split(', ')[1]))
            except:
                pass
            for i in range(self.ui.tabs.count()):
                self.ui.tabs.widget(i).chat_text.setFont(font)
        except:
            pass

        if settings.sections() == []:
            settings['Main'] = {'Language': 'Russian', 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'Enabled', 'MessagesHint': 'Disabled', 'MsgBacklight': 'Enabled', 'MsgFont': 'Consolas, 10', 'ParsingDebugger': 'Disabled'}
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
                self.child_widget.chat_text.setStyleSheet('selection-background-color: #ff7700')
                self.child_widget.members_list.setStyleSheet('selection-background-color: #ff7700')
                if self.child_widget.message_text.isEnabled() == True:
                    self.child_widget.message_text.setStyleSheet('selection-background-color: #ff7700')
                self.child_widget.verticalScrollBar.setStyleSheet('QScrollBar:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: #ff7700;\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_light.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_light.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
                self.child_widget.verticalScrollBar_2.setStyleSheet('QScrollBar:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: #ff7700;\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_light.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_light.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
            else:
                self.ui.line.setStyleSheet('color: #4a4a4a')
                self.child.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
                self.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
                self.ui.menubar.setStyleSheet('selection-background-color: #a14b00; selection-color: #ffffff')
                self.ui.conn_quality_progr.setStyleSheet('selection-background-color: #a14b00')
                self.child_widget.chat_text.setStyleSheet('selection-background-color: #a14b00')
                self.child_widget.members_list.setStyleSheet('selection-background-color: #a14b00')
                if self.child_widget.message_text.isEnabled() == True:
                    self.child_widget.message_text.setStyleSheet('selection-background-color: #a14b00')
                self.child_widget.verticalScrollBar.setStyleSheet('QScrollBar:vertical {border: 0px solid;\nbackground: rgb(43, 43, 43);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: rgb(161, 75, 0);\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_dark.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_dark.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
                self.child_widget.verticalScrollBar_2.setStyleSheet('QScrollBar:vertical {border: 0px solid;\nbackground: rgb(43, 43, 43);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: rgb(161, 75, 0);\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_dark.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_dark.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')

        #swiz001 = SettingsWizard001()
        if settings.sections() == [] or profiles.sections == []:
            self.child.show()
        if settings['Main']['DarkTheme'] == 'Disabled':
            self.child.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            for i in range(self.ui.tabs.count()):
                tab = self.ui.tabs.widget(i)
                tab.setStyleSheet('background-color: #ffffff;\ncolor: #000000;\nselection-background-color: #ff7700')
            self.child.ui.tableWidget.setStyleSheet('border-color: #ff7700; selection-background-color: #ff7700')
            self.child.ui.language_combo.setStyleSheet('border-color: #ff7700; selection-background-color: #ff7700')
        else:
            self.child.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            self.child.ui.tableWidget.setStyleSheet('border-color: #ff7700; selection-background-color: #a14b00')
            self.child.ui.language_combo.setStyleSheet('border-color: #ff7700; selection-background-color: #a14b00')
            for i in range(self.ui.tabs.count()):
                tab = self.ui.tabs.widget(i)
                tab.setStyleSheet('background-color: #313131;\ncolor: #ffffff;\nselection-background-color: #a14b00')
        try:
            self.child.ui.language_combo.setCurrentText(settings['Main']['Language'])
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
            print("\n".join(ex))
        try:
            self.child_5.ui.language_combo.setCurrentText(settings['Main']['Language'])
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
            print("\n".join(ex))
        self.child.ui.language_combo.currentIndexChanged.connect(self.change_language)

    def change_language(self):
        sconsole.change_language(self, settings, translator, sys, traceback)

    def about_window(self):
        settings.read('settings')
        self.version = version
        if settings.sections() == []:
            settings['Main'] = {'Language': 'Russian', 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'True', 'MessagesHint': 'Disabled', 'MsgBacklight': 'False', 'MsgFont': 'Consolas'}
            with open('settings', 'w') as configfile:
                settings.write(configfile)
            translator.translate_004(self, self.child_4.ui, 'Russian', en_US, ru_RU)
        else:
            translator.translate_004(self, self.child_4.ui, settings['Main']['Language'], en_US, ru_RU)
            if settings['Main']['DarkTheme'] == 'Disabled':
                self.child_4.setStyleSheet('background-color: #ffffff;\ncolor: #000000;\nselection-background-color: #ff7700')
            else:
                self.child_4.setStyleSheet('background-color: #313131;\ncolor: #ffffff;\nselection-background-color: #a14b00')
        self.child_4.exec_()


    def settings_window(self):
        settings.read('settings')
        self.child_5.ui.language_combo.clear()
        self.child_5.ui.language_combo.addItem('Russian')
        self.child_5.ui.language_combo.addItem('English')
        self.version = version
        if settings.sections() == []:
            settings['Main'] = {'Language': 'Russian', 'ColorScheme': 'Orange', 'DarkTheme': 'Enabled', 'MsgHistory': 'True', 'MessagesHint': 'Disabled', 'MsgBacklight': 'False', 'MsgFont': 'Consolas', 'ParsingDebugger': 'Disabled'}
            with open('settings', 'w') as configfile:
                settings.write(configfile)
            settings.read('settings')
        else:
            translator.translate_005(self, self.child_5.ui, settings['Main']['Language'], en_US, ru_RU)
            settings.read('settings')
            try:
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
                if settings['Main']['Language'] == 'Russian':
                    self.child_5.ui.language_combo.setCurrentText('Russian')
                else:
                    self.child_5.ui.language_combo.setCurrentText('English')
                if settings['Main']['MsgBacklight'] == 'Disabled':
                    self.child_5.ui.backlight_cb.setCheckState(0)
                else:
                    self.child_5.ui.save_msghistory_cb.setCheckState(2)
                if settings['Main']['MsgBacklight'] == 'Disabled':
                    self.child_5.ui.backlight_cb.setCheckState(0)
                else:
                    self.child_5.ui.backlight_cb.setCheckState(2)
                if settings['Main']['ParsingDebugger'] == 'Disabled':
                    self.child_5.ui.parsing_debugger_cb.setCheckState(0)
                else:
                    self.child_5.ui.backlight_cb.setCheckState(2)
                self.child_5.ui.msgfont_combo.setCurrentFont(QFont(settings['Main']['MsgFont'].split(', ')[0]))
                self.child_5.ui.font_size_sb.setValue(int(settings['Main']['MsgFont'].split(', ')[1]))
            except Exception as e:
                print(e)
        self.child_5.ui.buttonBox.accepted.connect(self.save_settings)
        self.child_5.ui.dark_theme_cb.stateChanged.connect(self.change_theme)
        self.child_5.exec_()

    def change_theme(self):
        sconsole.change_theme(self)

    def save_settings(self):
        sconsole.save_settings(self, settings, QFont, translator, sys, traceback, en_US, ru_RU)

    def connect_window(self):
        self.child.ui.language_label.setVisible(False)
        self.child.ui.language_combo.setVisible(False)
        if settings['Main']['DarkTheme'] == 'Disabled':
            self.child.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
        else:
            self.child.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
        self.child.exec_()

    def closeEvent(self, event):
        print('Quiting...')
        try:
            self.child.socket.close()
            self.child.thread.stop()
        except:
            pass
        self.close()

    def quit_app(self):
        try:
            self.child.socket.close()
            self.child.thread.stop()
        except:
            pass
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
                profiles[str(self.ui.profname_box.text())] = {'AuthMethod': self.ui.authmethod_combo.currentText(), 'Nicknames': profiles[str(self.ui.profname_box.text())]['Nicknames'], 'RealName': self.ui.realname_box.text(), 'Server': self.ui.server_box.text(), 'Port': str(self.ui.port_box.value()), 'Password': enc_password.decode('UTF-8'), 'EncryptCode': encrypt_code.decode('UTF-8'), 'Encoding': 'cp866', 'QuitingMsg': self.ui.quiting_msg_box.text(), 'HostName': self.ui.hostname_box.text()}
            elif self.ui.encoding_combo.currentText() == 'KOI8-R':
                profiles[str(self.ui.profname_box.text())] = {'AuthMethod': self.ui.authmethod_combo.currentText(), 'Nicknames': profiles[str(self.ui.profname_box.text())]['Nicknames'], 'RealName': self.ui.realname_box.text(), 'Server': self.ui.server_box.text(), 'Port': str(self.ui.port_box.value()), 'Password': enc_password.decode('UTF-8'), 'EncryptCode': encrypt_code.decode('UTF-8'), 'Encoding': 'koi8_r', 'QuitingMsg': self.ui.quiting_msg_box.text(), 'HostName': self.ui.hostname_box.text()}
            elif self.ui.encoding_combo.currentText() == 'KOI8-U':
                profiles[str(self.ui.profname_box.text())] = {'AuthMethod': self.ui.authmethod_combo.currentText(), 'Nicknames': profiles[str(self.ui.profname_box.text())]['Nicknames'], 'RealName': self.ui.realname_box.text(), 'Server': self.ui.server_box.text(), 'Port': str(self.ui.port_box.value()), 'Password': enc_password.decode('UTF-8'), 'EncryptCode': encrypt_code.decode('UTF-8'), 'Encoding': 'koi8_u', 'QuitingMsg': self.ui.quiting_msg_box.text(), 'HostName': self.ui.hostname_box.text()}
            else:
                profiles[str(self.ui.profname_box.text())] = {'AuthMethod': self.ui.authmethod_combo.currentText(), 'Nicknames': profiles[str(self.ui.profname_box.text())]['Nicknames'], 'RealName': self.ui.realname_box.text(), 'Server': self.ui.server_box.text(), 'Port': str(self.ui.port_box.value()), 'Password': enc_password.decode('UTF-8'), 'EncryptCode': encrypt_code.decode('UTF-8'), 'Encoding': self.ui.encoding_combo.currentText(), 'QuitingMsg': self.ui.quiting_msg_box.text(), 'HostName': self.ui.hostname_box.text()}
            if self.ui.requiredssl_cb.checkState() == 0:
                profiles[str(self.ui.profname_box.text())]['SSL'] = 'Disabled'
            else:
                profiles[str(self.ui.profname_box.text())]['SSL'] = 'Enabled'
            if self.ui.authmethod_combo.currentText() == en_US.get()['w_o_auth'] or self.ui.authmethod_combo.currentText() == ru_RU.get()['w_o_auth']:
                profiles[str(self.ui.profname_box.text())]['AuthMethod'] = 'Disabled'
            else:
                profiles[str(self.ui.profname_box.text())]['AuthMethod'] = self.ui.authmethod_combo.currentText()
            with open('profiles', 'w') as configfile:
                profiles.write(configfile)
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
            print("\n".join(ex))

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
            exc_type, exc_value, exc_tb = sys.exc_info()
            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
            print("\n".join(ex))
        if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
            self.ui.nicknames_combo.addItem(ru_RU.get()['makenick'])
        elif settings.sections() != [] and settings['Main']['Language'] == 'English':
            self.ui.nicknames_combo.addItem(en_US.get()['makenick'])
        self.ui.clear_nicknames_btn.setEnabled(False)
        self.ui.clear_nicknames_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
        self.timer.start(100)

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
                profiles[str(self.ui.lineEdit.text())] = {'AuthMethod': '', 'Nicknames': '', 'RealName': '', 'Server': '', 'Port': '', 'Encoding': '', 'QuitingMsg': 'Tinelix IRC Client ver. {0} ({1})'.format(version, date), 'HostName': ''}
                profiles[str(self.ui.lineEdit.text())]['SSL'] = 'Disabled'
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
                else:
                    swiz003.ui.nicknames_combo.addItem('')
                    swiz003.ui.clear_nicknames_btn.setEnabled(False)
                    swiz003.ui.clear_nicknames_btn.setStyleSheet('color: #4f4f4f')
                swiz003.ui.realname_box.setText(profiles[str(self.ui.lineEdit.text())]['RealName'])
                swiz003.ui.hostname_box.setText(profiles[str(self.ui.lineEdit.text())]['HostName'])
                if profiles[str(self.ui.lineEdit.text())]['SSL'] == 'Enabled':
                    swiz003.ui.requiredssl_cb.setCheckState(2)
                else:
                    swiz003.ui.requiredssl_cb.setCheckState(0)
            except Exception as e:
                if swiz003.ui.nicknames_combo.count() == 0:
                    swiz003.ui.nicknames_combo.addItem('')
            try:
                if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                    swiz003.ui.nicknames_combo.addItem(ru_RU.get()['makenick'])
                elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                    swiz003.ui.nicknames_combo.addItem(en_US.get()['makenick'])
                if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                    swiz003.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
                elif settings.sections() != [] and settings['Main']['DarkTheme'] == 'Enabled':
                    swiz003.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            except:
                pass
            swiz003.ui.encoding_combo.addItem('UTF-8')
            swiz003.ui.encoding_combo.addItem('Windows-1251')
            swiz003.ui.encoding_combo.addItem('DOS (866)')
            swiz003.ui.encoding_combo.addItem('KOI8-R')
            swiz003.ui.encoding_combo.addItem('KOI8-U')
            swiz003.ui.authmethod_combo.addItem('NickServ')
            try:
                if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                    swiz003.ui.authmethod_combo.addItem(ru_RU.get()['w_o_auth'])
                elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                    swiz003.ui.authmethod_combo.addItem(en_US.get()['w_o_auth'])
                if profiles[str(self.ui.lineEdit.text())]['AuthMethod'] == 'Disabled':
                    if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                        swiz003.ui.authmethod_combo.setCurrentText(ru_RU.get()['w_o_auth'])
                    elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                        swiz003.ui.authmethod_combo.setCurrentText(en_US.get()['w_o_auth'])
            except:
                pass
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
                swiz003.ui.encoding_combo.setCurrentText(profiles[str(self.ui.lineEdit.text())]['Encoding'])
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
                swiz003.ui.realname_box.setText(profiles[str(self.ui.lineEdit.text())]['RealName'])
                swiz003.ui.hostname_box.setText(profiles[str(self.ui.lineEdit.text())]['HostName'])
                if profiles[str(self.ui.lineEdit.text())]['SSL'] == 'Enabled':
                    swiz003.ui.requiredssl_cb.setCheckState(2)
                else:
                    swiz003.ui.requiredssl_cb.setCheckState(0)
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
            try:
                if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                    swiz003.ui.authmethod_combo.addItem(ru_RU.get()['w_o_auth'])
                elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                    swiz003.ui.authmethod_combo.addItem(en_US.get()['w_o_auth'])
                if profiles[str(self.ui.lineEdit.text())]['AuthMethod'] == 'Disabled':
                    if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                        swiz003.ui.authmethod_combo.setCurrentText(ru_RU.get()['w_o_auth'])
                    elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                        swiz003.ui.authmethod_combo.setCurrentText(en_US.get()['w_o_auth'])
            except:
                pass
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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        self.progr = ProgressDlg(self)
        self.progr.ui.frame.setVisible(False)
        self.progr.ui.additional_btn.clicked.connect(self.progress_additional)
        self.channel = None
        self.timer = QTimer()
        self.connected = False
        self.timer.timeout.connect(self.tick)
        self.timer.start(100)
        self.sections_count = None
        self.members = []
        self.operators = []
        self.owners = []
        self.channels = {}
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
        ping_count = 0
        self.thread.started.connect(self.started)
        self.thread.start()
        self.connected = True
        self.now = datetime.datetime.now()
        self.parent.child_widget.message_text.setText('')
        self.parent.child_widget.message_text.setEnabled(True)
        self.parent.ui.join_item.setEnabled(True)
        self.parent.ui.msg_history.setEnabled(True)
        self.parent.ui.join_item.triggered.connect(self.join_channel)
        if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
            self.parent.child_widget.message_text.setStyleSheet('selection-background-color: rgb(255, 119, 0); color: #000000')
        else:
            self.parent.child_widget.message_text.setStyleSheet('selection-background-color: rgb(161, 75, 0); color: #ffffff')
        if self.parent.child_widget.message_text.text() != '':
            self.parent.child_widget.send_msg_btn.setEnabled(True)
            if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                self.parent.child_widget.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
            else:
               self.parent.child_widget.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
            self.parent.child_widget.message_text.returnPressed.connect(self.send_msg)
        else:
            self.parent.child_widget.send_msg_btn.setEnabled(False)
            self.parent.child_widget.send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
        self.parent.child_widget.send_msg_btn.clicked.connect(self.send_msg)
        self.parent.child_widget.message_text.textChanged.connect(self.msgtext_changing)
        settings.read('settings')
        if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
            self.ui.connect_btn.setText(ru_RU.get()['dscn_btn'])
        elif settings.sections() != [] and settings['Main']['Language'] == 'English':
            self.ui.connect_btn.setText(en_US.get()['dscn_btn'])
        self.ui.connect_btn.clicked.disconnect()
        self.ui.connect_btn.clicked.connect(self.irc_disconnect)

    def msgtext_changing(self):
        if self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text() != '':
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).send_msg_btn.setEnabled(True)
            self.contextMenu = QMenu(self)
            try:
                if self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text() == '/' and settings.sections() != [] and settings['Main']['MessagesHint'] == 'Enabled':
                    settings.read('settings')
                    commands_list = ['/nickserv', '/list', '/join', '/names', '/whois', '/part', '/quit']
                    try:
                        commands = QCompleter(commands_list, self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text)
                        self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setCompleter(commands)
                    except Exception as e:
                        exc_type, exc_value, exc_tb = sys.exc_info()
                        ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                        print("\n".join(ex))
            except:
                pass
            settings.read('settings')
            try:
                if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                    for i in range(self.parent.ui.tabs.count()):
                        self.parent.ui.tabs.widget(i).send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
                        self.parent.ui.tabs.widget(i).message_text.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #000000')
                else:
                    for i in range(self.parent.ui.tabs.count()):
                        self.parent.ui.tabs.widget(i).send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
                        self.parent.ui.tabs.widget(i).message_text.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #ffffff')
                if self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.isEnabled == False:
                    self.parent.ui.tabs.widget(i).send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
                    self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).send_msg_btn.setEnabled(False)
            except:
                pass
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.returnPressed.connect(self.send_msg)
        else:
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).send_msg_btn.setEnabled(False)
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).send_msg_btn.setStyleSheet('border-color: rgb(255, 119, 0); selection-background-color: rgb(255, 119, 0); color: #4f4f4f')
            try:
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.returnPressed.disconnect()
            except:
                pass
    @QtCore.pyqtSlot()
    def command_choosed(self):
        command = self.sender()
        if command == self.signin_item:
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setText('/nickserv')
        elif command == self.chanlist_item:
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setText('/list')
        elif command == self.joinch_item:
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setText('/join #')
        elif command == self.names_item:
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setText('/names')
        elif command == self.whois_item:
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setText('/whois')
        elif command == self.part_item:
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setText('/part')
        elif command == self.quit_item:
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setText('/quit')

    def irc_disconnect(self):
        try:
            profiles.read('profiles')
            print('Disconnecting...')
            self.socket.send(bytes('QUIT {0}\r\n'.format(profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['quitingmsg']), self.encoding))
            self.socket.close()
            self.parent.child_widget.send_msg_btn.setEnabled(False)
            self.parent.child_widget.message_text.setEnabled(False)
            self.ui.connect_btn.clicked.connect(self.irc_connect)
            settings.read('settings')
            if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                self.ui.connect_btn.setText(ru_RU.get()['conn_btn'])
            elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                self.ui.connect_btn.setText(en_US.get()['conn_btn'])
            self.timer.start()
            self.parent.child_widget.members_list.clear()
            self.parent.child_widget.members_list.setVisible(False)
            self.parent.ui.conn_quality_progr.setValue(0)
            self.parent.ui.latency_label.setText('')
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
            print("\n".join(ex))

    @QtCore.pyqtSlot(str, str, float, str, str, str, float, socket.socket)
    def started(self, status, server, port, nickname, encoding, quiting_msg, ping, socket):
        self.socket = socket
        self.encoding = encoding
        self.server = server
        self.port = port
        self.nickname = nickname
        self.quiting_msg = quiting_msg
        self.parent.setWindowTitle('Tinelix IRC Client | {0}'.format(self.server))
        parser.parse(self, settings, status, sys, traceback, datetime, os, time, en_US, ru_RU)

    def irc_reconnect(self):
        self.thread.start()
        self.timer.stop()

    def irc_reconnect_msg(self):
        self.parent.child_widget.chat_text.setHtml('{0}\nReconnecting...'.format(self.parent.child_widget.chat_text.toHtml()))
        self.timer_2.stop()

    def progress_additional(self):
        if self.progr.ui.frame.isVisible() == False:
            self.progr.ui.frame.setVisible(True)
        else:
            self.progr.ui.frame.setVisible(False)

    def send_msg(self):
        if self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/join '):
            msg_list = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')
            if self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/join #'):
                self.socket.send(bytes('JOIN {0}\r\n'.format(msg_list[1]), self.encoding))
                self.channel = msg_list[1]
                if self.parent.ui.leave_item.isEnabled() == False:
                    self.parent.ui.leave_item.setEnabled(True)
                    self.parent.ui.leave_item.triggered.connect(self.leave_channel)
            else:
                self.socket.send(bytes('JOIN #{0}\r\n'.format(msg_list[1]), self.encoding))
                self.channel = '#{0}'.format(msg_list[1])
            self.tab = ChatWidget()
            try:
                settings.read('settings')
                if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                    self.tab.setStyleSheet('background-color: #ffffff;\ncolor: #000000;\nselection-background-color: rgb(255, 119, 0);')
                    self.tab.chat_text.setStyleSheet('selection-background-color: rgb(255, 119, 0);')
                    self.tab.members_list.setStyleSheet('selection-background-color: #ff7700;')
                    self.tab.verticalScrollBar.setStyleSheet('QScrollBar:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: #ff7700;\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_light.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_light.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
                    self.tab.verticalScrollBar_2.setStyleSheet('QScrollBar:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: #a14b00;\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_light.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_light.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
                else:
                    self.tab.setStyleSheet('background-color: #313131;\ncolor: #ffffff;\nselection-background-color: rgb(161, 75, 0);')
                    self.tab.chat_text.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
                    self.tab.members_list.setStyleSheet('selection-background-color: #a14b00;')
                    self.tab.verticalScrollBar.setStyleSheet('QScrollBar:vertical {border: 0px solid;\nbackground: rgb(43, 43, 43);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: rgb(161, 75, 0);\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_dark.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_dark.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
                    self.tab.verticalScrollBar_2.setStyleSheet('QScrollBar:vertical {border: 0px solid;\nbackground: rgb(43, 43, 43);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: rgb(161, 75, 0);\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_dark.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_dark.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')

                if settings.sections != [] and settings['Main']['Language'] == 'Russian':
                    self.tab.error_getting_member_list.setText(ru_RU.get()['mbgt_err'])
                    self.tab.close_panel_btn.setText(ru_RU.get()['mbget_cl'])
                else:
                    self.tab.error_getting_member_list.setText(en_US.get()['mbgt_err'])
                    self.tab.close_panel_btn.setText(en_US.get()['mbget_cl'])

                self.tab.members_list.setContextMenuPolicy(Qt.CustomContextMenu)
                self.tab.members_list.customContextMenuRequested.connect(self.call_member_cm)
                self.tab.members_list.setVisible(False);
                self.tab.list_frame.setVisible(True);
                self.member_context_menu = QMenu(self)
                self.parent.ui.tabs.addTab(self.tab, self.channel)
                self.tab.chat_text.setVerticalScrollBar(self.tab.verticalScrollBar)
                self.tab.members_list.setVerticalScrollBar(self.tab.verticalScrollBar_2)
                self.tab.close_panel_btn.clicked.connect(self.close_member_error_panel)
                self.tab.message_text.setEnabled(True)
                self.tab.send_msg_btn.setEnabled(False)
                self.tab.send_msg_btn.clicked.connect(self.send_msg)
                font = QFont(settings['Main']['MsgFont'].split(', ')[0])
                try:
                    font.setPointSize(int(settings['Main']['MsgFont'].split(', ')[1]))
                except:
                    pass
                for i in range(self.parent.ui.tabs.count()):
                    self.parent.ui.tabs.widget(i).chat_text.setFont(font)
                    self.parent.ui.tabs.widget(i).chat_text.setHtml(self.parent.child_widget.chat_text.toHtml())
                    self.parent.ui.tabs.widget(i).message_text.setText('')
                self.timer = QTimer()
                self.timer.timeout.connect(self.chanjoined)
                self.timer.start(100)
                self.tab.message_text.textChanged.connect(self.msgtext_changing)
                if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                    self.tab.message_text.setStyleSheet('selection-background-color: rgb(255, 119, 0); color: #000000')
                else:
                    self.tab.message_text.setStyleSheet('selection-background-color: rgb(161, 75, 0); color: #ffffff')
            except Exception as e:
                exc_type, exc_value, exc_tb = sys.exc_info()
                ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                print("\n".join(ex))
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/whois'):
            try:
                msg_list = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')
                nick = msg_list[1]
                self.socket.send(bytes('WHOIS {0}\r\n'.format(msg_list[1]), self.encoding))
            except:
                self.socket.send(bytes('WHOIS\r\n', self.encoding))
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.moveCursor(QTextCursor.End)
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/list'):
            try:
                msg_list = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')
                self.socket.send(bytes('LIST\r\n', self.encoding))
            except:
                pass
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.moveCursor(QTextCursor.End)
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text() == ('/leave') or self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text() == ('/part'):
            try:
                msg_list = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')
                self.socket.send(bytes('PART {0}\r\n'.format(self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex())), self.encoding))
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).members_list.clear()
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).members_list.setVisible(False)
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setEnabled(False)
                for i in range(self.parent.ui.tabs.count()):
                    if i > 0 and self.parent.ui.tabs.tabText(i) == self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()):
                        self.parent.ui.tabs.removeTab(i)
                if settings.sections() != [] and settings['Main']['Language'] == 'English':
                    self.parent.ui.status_label.setText(en_US.get()['rdstatus'])
                else:
                    self.parent.ui.status_label.setText(ru_RU.get()['rdstatus'])
            except:
                pass
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/names') or self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/members'):
            try:
                msg_list = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')
                for i in range(self.parent.ui.tabs.count()):
                    self.parent.ui.tabs.widget(i).members_list.clear()
                self.socket.send(bytes('NAMES {0}\r\n'.format(msg_list[1]), self.encoding))
            except:
                self.socket.send(bytes('NAMES {0}\r\n'.format(self.channel), self.encoding))
            self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.moveCursor(QTextCursor.End)
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/msg'):
            msg_list = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')
            self.socket.send(bytes('PRIVMSG {0}\r\n'.format(' '.join(msg_list[1:])), self.encoding))
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text() == '/info':
            try:
                self.socket.send(bytes('INFO\r\n', self.encoding))
            except:
                pass
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/ping'):
            try:
                msg_list = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')
                self.socket.send(bytes('PING {0}\r\n'.format(msg_list[1]), self.encoding))
            except:
                pass
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/ctcp') and len(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')) == 3:
            if(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')[2] == 'version'):
                self.socket.send(bytes('PRIVMSG {0} \001VERSION\001\r\n'.format(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')[1]), self.encoding))
            elif(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')[2] == 'clientinfo'):
                self.socket.send(bytes('PRIVMSG {0} \001CLIENTINFO\001\r\n'.format(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')[1]), self.encoding))
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text() == '/disconnect' or self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/quit'):
            settings.read('settings')
            self.socket.send(bytes('QUIT {0}\r\n'.format(self.quiting_msg), self.encoding))
            self.socket.close()
            for i in range(self.parent.ui.tabs.count()):
                if i > 0 and self.parent.ui.tabs.tabText(i) == self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()):
                    self.parent.ui.tabs.removeTab(i)
            self.ui.connect_btn.clicked.connect(self.irc_connect)
            if settings.sections() != [] and settings['Main']['Language'] == 'English':
                self.ui.connect_btn.setText(en_US.get()['conn_btn'])
            else:
                self.ui.connect_btn.setText(ru_RU.get()['conn_btn'])
            self.parent.child_widget.members_list.clear()
            self.parent.child_widget.members_list.setVisible(False)
            self.parent.setWindowTitle('Tinelix IRC Client')
            if settings.sections() != [] and settings['Main']['Language'] == 'English':
                self.parent.child_widget.message_text.setText(en_US.get()['cantsmsg'])
            else:
                self.parent.child_widget.message_text.setText(ru_RU.get()['cantsmsg'])
            self.parent.ui.conn_quality_progr.setValue(0)
            self.parent.ui.latency_label.setText('')
            self.parent.child_widget.message_text.setEnabled(False)
            self.server = None
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/'):
            try:
                msg_list = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')
                self.socket.send(bytes('{0}\r\n'.format(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text()[1:]), self.encoding))
            except Exception as e:
                exc_type, exc_value, exc_tb = sys.exc_info()
                ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                print("\n".join(ex))
        elif self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()) != 'Thread' and self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()) != 'Поток':
            for i in range(self.parent.ui.tabs.count()):
                if self.parent.ui.tabs.tabText(i) == self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()):
                    self.socket.send(bytes('PRIVMSG {0} :{1}\r\n'.format(self.parent.ui.tabs.tabText(i), self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text()), self.encoding))
        if self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/nickserv identify'):
            if settings['Main']['MsgBacklight'] == 'Disabled':
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.setHtml('{0}{1}: {2} [password] ({3})'.format(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.toHtml(), self.nickname, ' '.join(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')[:2]), datetime.datetime.now().strftime("%H:%M:%S")))
            else:
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.setHtml('{0}<b>{1}:</b> {2} [password] <span style="font-size: 10px">({3})</span>'.format(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.toHtml(), self.nickname, ' '.join(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().split(' ')[:2]), datetime.datetime.now().strftime("%H:%M:%S")))
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text().startswith('/nick'):
            try:
                msg_list = self.parent.child_widget.message_text.text().split(' ')
                nick = msg_list[1]
                self.socket.send(bytes('NICK {0}\r\n'.format(msg_list[1]), self.encoding))
            except:
                self.socket.send(bytes('NICK\r\n', self.encoding))
        elif self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text() != '' and self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text() != ' ' and self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.isEnabled() == True:
            if settings['Main']['MsgBacklight'] == 'Disabled':
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.setHtml('{0}\n{1}: {2} ({3})'.format(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.toHtml(), self.nickname, self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text(), datetime.datetime.now().strftime("%H:%M:%S")))
            else:
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.setHtml('{0}<b>{1}:</b> {2} <span style="font-size: 10px">({3})</span>'.format(self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.toHtml(), self.nickname, self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.text(), datetime.datetime.now().strftime("%H:%M:%S")))
        self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setText('')
        self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.moveCursor(QTextCursor.End)

    def leave_channel(self):
        for i in range(self.parent.ui.tabs.count()):
            if i > 0 and i == self.parent.ui.tabs.currentIndex():
                try:
                    self.socket.send(bytes('PART {0}\r\n'.format(self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex())), self.encoding))
                    self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).members_list.clear()
                    self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).members_list.setVisible(False)
                    self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setEnabled(False)
                    self.parent.ui.tabs.removeTab(self.parent.ui.tabs.currentIndex())
                    if settings.sections() != [] and settings['Main']['Language'] == 'English':
                        self.parent.ui.status_label.setText(en_US.get()['rdstatus'])
                    else:
                        self.parent.ui.status_label.setText(ru_RU.get()['rdstatus'])
                except:
                    pass

    def join_channel(self):
        self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).message_text.setText('/join #')

    def show_channel_history(self):
        try:
            webbrowser.open('file://{0}/history/irc_{1}_{2}_{3}.html'.format(os.getcwd(), self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()), self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text(), self.now.strftime('%Y-%m-%d_%H.%M.%S')))
        except Exception as e:
            print(e)

    def chanjoined(self):
        tabs_count = self.parent.ui.tabs.count() - 1
        self.parent.ui.tabs.setCurrentIndex(tabs_count)
        try:
            self.socket.send(bytes('TOPIC {0}\r\n'.format(self.channel), self.encoding))
        except:
            pass
        self.timer.stop()

    def call_member_cm(self, pos):
        self.tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
        try:
            if self.tab.members_list.currentItem().parent() != None:
                nick_action = QtWidgets.QWidgetAction(self.member_context_menu)
                nick_label = QtWidgets.QLabel(self.tab.members_list.currentItem().text(0))
                nick_action.setDefaultWidget(nick_label)
                nick_action.setEnabled(False)
                self.member_context_menu.clear()
                try:
                    settings.read('settings')
                    if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Enabled':
                        nick_label.setStyleSheet('QLabel {margin-left: 13px;\nfont-weight: 700; color: #828282}')
                    elif settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                        nick_label.setStyleSheet('QLabel {margin-left: 13px;\nfont-weight: 700; color: #626262}')
                    else:
                        nick_label.setStyleSheet('QLabel {margin-left: 13px;\nfont-weight: 700;}')
                except:
                    pass
                self.member_context_menu.addAction(nick_action)
                try:
                    if settings.sections() != [] and settings['Main']['Language'] == 'English':
                        self.mention_item = self.member_context_menu.addAction(en_US.get()['mntion_a'])
                        self.whoism_item = self.member_context_menu.addAction(en_US.get()['whoism_a'])
                        self.ping_item = self.member_context_menu.addAction(en_US.get()['pingctcp'])
                        self.check_client_version_item = self.member_context_menu.addAction(en_US.get()['ver_ctcp'])
                        self.clientinfo_item = self.member_context_menu.addAction(en_US.get()['clinctcp'])
                    else:
                        self.mention_item = self.member_context_menu.addAction(ru_RU.get()['mntion_a'])
                        self.whoism_item = self.member_context_menu.addAction(ru_RU.get()['whoism_a'])
                        self.ping_item = self.member_context_menu.addAction(ru_RU.get()['pingctcp'])
                        self.check_client_version_item = self.member_context_menu.addAction(ru_RU.get()['ver_ctcp'])
                        self.clientinfo_item = self.member_context_menu.addAction(ru_RU.get()['clinctcp'])
                except:
                    pass
                context_menu = self.member_context_menu.exec_(self.tab.members_list.mapToGlobal(QPoint(-self.member_context_menu.width() - 2, -0)))
        except:
            pass
        try:
            if context_menu == self.mention_item and self.tab.members_list.currentItem().text(0) != '':
                self.tab.message_text.setText(self.tab.members_list.currentItem().text(0))
            elif context_menu == self.whoism_item and self.tab.members_list.currentItem().text(0) != '':
                self.tab.message_text.setText('/whois {0}'.format(self.tab.members_list.currentItem().text(0)))
            elif context_menu == self.ping_item and self.tab.members_list.currentItem().text(0) != '':
                self.tab.message_text.setText('/ping {0}'.format(self.tab.members_list.currentItem().text(0)))
            elif context_menu == self.check_client_version_item and self.tab.members_list.currentItem().text(0) != '':
                self.tab.message_text.setText('/ctcp {0} version'.format(self.tab.members_list.currentItem().text(0)))
            elif context_menu == self.clientinfo_item and self.tab.members_list.currentItem().text(0) != '':
                self.tab.message_text.setText('/ctcp {0} clientinfo'.format(self.tab.members_list.currentItem().text(0)))
        except:
            pass

    def close_member_error_panel(self):
        self.tab.list_frame.setVisible(False)

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
        try:
            swiz003.ui.realname_box.setText(profiles[str(swiz003.ui.profname_box.text())]['RealName'])
            swiz003.ui.hostname_box.setText(profiles[str(swiz003.ui.profname_box.text())]['HostName'])
            if profiles[str(swiz003.ui.profname_box.text())]['SSL'] == 'Enabled':
                swiz003.ui.requiredssl_cb.setCheckState(2)
            else:
                swiz003.ui.requiredssl_cb.setCheckState(0)
        except:
            pass
        swiz003.ui.encoding_combo.addItem('UTF-8')
        swiz003.ui.encoding_combo.addItem('Windows-1251')
        swiz003.ui.encoding_combo.addItem('DOS (866)')
        swiz003.ui.encoding_combo.addItem('KOI8-R')
        swiz003.ui.encoding_combo.addItem('KOI8-U')
        swiz003.ui.authmethod_combo.addItem('NickServ')
        try:
            if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                swiz003.ui.authmethod_combo.addItem(ru_RU.get()['w_o_auth'])
            elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                swiz003.ui.authmethod_combo.addItem(en_US.get()['w_o_auth'])
            if profiles[str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())]['AuthMethod'] == 'Disabled':
                if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                    swiz003.ui.authmethod_combo.setCurrentText(ru_RU.get()['w_o_auth'])
                elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                    swiz003.ui.authmethod_combo.setCurrentText(en_US.get()['w_o_auth'])
        except:
            pass
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
            exc_type, exc_value, exc_tb = sys.exc_info()
            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
            print("\n".join(ex))
        translator.translate_003(self, swiz003.ui, settings['Main']['Language'], en_US, ru_RU)
        swiz003.exec_()

    def del_item(self):
        try:
            profiles.remove_section(str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()))
            with open('profiles', 'w') as configfile:
                profiles.write(configfile)
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
            print("\n".join(ex))
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
        self.ui.website_btn.clicked.connect(self.website_open)
        self.ui.pyqt_version.setText(PYQT_VERSION_STR);
        self.ui.qt_version.setText(QT_VERSION_STR);
        self.ui.python_version.setText("{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]));
        self.ui.platform.setText(platform.system());
        self.ui.platform_version.setText(platform.version());

    def repo_open(self):
        webbrowser.open('https://github.com/tinelix/irc-client')

    def website_open(self):
        webbrowser.open('https://tinelix.github.io');

class AdvancedSettingsDlg(QtWidgets.QDialog, ext_sett):
    def __init__(self, parent=None):
        super(AdvancedSettingsDlg, self).__init__(parent)
        self.ui = ext_sett()
        self.ui.setupUi(self)
        self.parent = parent
        settings.read('settings')
        if settings.sections() != []:
            self.ui.language_combo.setCurrentText(settings['Main']['Language'])

class ProgressDlg(QtWidgets.QDialog, progrdlg):
    def __init__(self, parent=None):
        super(ProgressDlg, self).__init__(parent)
        self.ui = progrdlg()
        self.ui.setupUi(self)
        self.parent = parent
        self.setWindowFlag(Qt.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        settings.read('settings')
        try:
            if settings.sections() != [] and settings['Main']['DarkTheme'] == 'Disabled':
                self.setStyleSheet('background-color: #ffffff; color: #000000;')
                self.progressBar.setStyleSheet('selection-background-color: #ff7700;')
            elif settings.sections() != [] and settings['Main']['DarkTheme'] == 'Enabled':
                self.setStyleSheet('background-color: #313131; color: #ffffff;')
                self.progressBar.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
        except:
            pass

class MentionNotificationWindow(QtWidgets.QDialog, mention_notif_window):
    def __init__(self, parent=None):
        super(MentionNotificationWindow, self).__init__(parent)
        self.parent = parent
        self.ui = mention_notif_window()
        self.ui.setupUi(self)
        self.ui.label_2.installEventFilter(self)
        self.ui.openclient_btn.clicked.connect(self.open_client)
        try:
            print('Test')
        except:
            pass
    def close_notification(self):
        self.hide()
        self.parent.hide()
        self.close()

    def open_client(self):
        self.hide()
        self.close()
        self.parent.setWindowState(Qt.WindowActive)

    def eventFilter(self, obj, e):
        if e.type() == 2:
            self.close_notification()
        return super(MentionNotificationWindow,self).eventFilter(obj,e)

app = QtWidgets.QApplication([])
app.setStyle('Fusion')
application = mainform()
application.show()

sys.exit(app.exec())
