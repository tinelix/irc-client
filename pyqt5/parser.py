from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def parse(self, settings, status, sys, traceback, datetime, os, time, en_US, ru_RU):
        settings.read('settings')
        text = '{}'.format(status)
        msg_list = status.splitlines()
        for msg_line in msg_list:
            try:
                if settings.sections() != [] and settings['Main']['ParsingDebugger'] == 'Enabled':
                    print(msg_line)
            except:
                pass
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
                        if settings.sections() != [] and settings['Main']['Language'] == 'English':
                            self.parent.ui.status_label.setText(en_US.get()['rdstatus'])
                        else:
                            self.parent.ui.status_label.setText(ru_RU.get()['rdstatus'])
                    else:
                       self.parent.ui.conn_quality_progr.setValue(0)
                       self.parent.ui.latency_label.setText('')
                except:
                    pass
            elif msg_line.startswith('{0} PONG'.format(self.server)):
                decoded_text = status.split(' ')
                for i in range(self.parent.ui.tabs.count()):
                    if self.parent.ui.tabs.tabText(i) == self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()):
                        tab = self.parent.ui.tabs.widget(i)
                        if settings['Main']['MsgBacklight'] == 'Disabled':
                            tab.chat_text.setHtml('{0}\n{1}: Pong! ({2})'.format(tab.chat_text.toHtml(), decoded_text[3].splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        else:
                            tab.chat_text.setHtml('{0}<b>{1}:</b> Pong! <span style="font-size: 10px">({2})</span>'.format(tab.chat_text.toHtml(), decoded_text[3].splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 353') != -1:
                try:
                    self.names_raw = msg_line.split(' ')[5:]
                    for nick in self.names_raw:
                        if nick.startswith('@') and nick != '' and nick != ' ':
                            self.operators.append(nick.replace(':', '').replace('&', '').replace('@', ''))
                        elif nick.startswith('~') and nick != '' and nick != ' ':
                            self.owners.append(nick.replace(':', '').replace('~', '').replace('&', '').replace('@', ''))
                        elif nick != '' and nick != ' ':
                            self.members.append(nick.replace(':', '').replace('~', '').replace('&', ''))
                except Exception as e:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 366') != -1:
                decoded_text = status.split(' ')
                try:
                    if settings['Main']['Language'] == 'English':
                        owners_list = QTreeWidgetItem(['{0} ({1})'.format(en_US.get()['owners'], len(self.owners))])
                        operators_list = QTreeWidgetItem(['{0} ({1})'.format(en_US.get()['oprtors'], len(self.operators))])
                        members_list = QTreeWidgetItem(['{0} ({1})'.format(en_US.get()['members'], len(self.members))])
                    else:
                        owners_list = QTreeWidgetItem(['{0} ({1})'.format(ru_RU.get()['owners'], len(self.owners))])
                        operators_list = QTreeWidgetItem(['{0} ({1})'.format(ru_RU.get()['oprtors'], len(self.operators))])
                        members_list = QTreeWidgetItem(['{0} ({1})'.format(ru_RU.get()['members'], len(self.members))])
                    for operator in self.operators:
                        if operator != '':
                            child = QTreeWidgetItem([operator])
                            operators_list.addChild(child)
                            operators_list.setStatusTip(0, operator)
                    for member in self.members:
                        if member != '':
                            child = QTreeWidgetItem([member])
                            members_list.addChild(child)
                            operators_list.setToolTip(0, member)
                    for owner in self.owners:
                        if owner != '':
                            child = QTreeWidgetItem([owner])
                            owners_list.addChild(child)
                            operators_list.setToolTip(0, owner)
                    for i in range(self.parent.ui.tabs.count()):
                        if self.parent.ui.tabs.tabText(i) == self.channel:
                            tab = self.parent.ui.tabs.widget(i)
                            tab.members_list.clear()
                            tab.members_list.addTopLevelItems([owners_list, operators_list, members_list])
                            tab.members_list.setVisible(True);
                            tab.list_frame.setVisible(False);
                    operators_list.setIcon(0, QIcon(':/icons/operator_icon.png'))
                    operators_list.setExpanded(True)
                    members_list.setIcon(0, QIcon(':/icons/member_icon.png'))
                    members_list.setExpanded(True)
                    owners_list.setIcon(0, QIcon(':/icons/owner_icon.png'))
                    owners_list.setExpanded(True)
                    self.members = []
                    self.operators = []
                    self.owners = []
                except Exception as e:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
                    self.parent.child_widget.members_list.setVisible(False);
                    self.parent.child_widget.list_frame.setVisible(True);
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 372') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    if settings['Main']['MsgBacklight'] == 'Disabled':
                        tab.chat_text.setHtml('{0}\nMOTD: {1}'.format(tab.chat_text.toHtml(), "".join(" ".join(msg_line.split(' ')[3:]).splitlines()[0:]).replace('<', '&#60;').replace('>', '&#62;')))
                    else:
                        tab.chat_text.setHtml('{0}\n<b><i>MOTD:</i></b> {1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[3:]).replace('<', '&#60;').replace('>', '&#62;')))
                except:
                    tab.chat_text.setHtml('{0}\nMOTD: {1}'.format(tab.chat_text.toHtml(), "".join(" ".join(msg_line.split(' ')[3:]).splitlines()[0]).replace('<', '&#60;').replace('>', '&#62;')))
                tab.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 371') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    if settings['Main']['MsgBacklight'] == 'Disabled':
                        tab.chat_text.setHtml('{0}\nInfo: {1}'.format(tab.chat_text.toHtml(), "".join(" ".join(msg_line.split(' ')[3:]).splitlines()[0:])))
                    else:
                        tab.chat_text.setHtml('{0}\n<b><i>Info:</i></b> {1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[3:])))
                except:
                    tab.chat_text.setHtml('{0}\nInfo: {1}'.format(tab.chat_text.toHtml(), "".join(" ".join(msg_line.split(' ')[3:]).splitlines()[0])))
                tab.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 671') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    if settings['Main']['MsgBacklight'] == 'Disabled':
                        tab.chat_text.setHtml('{0}\n{1} using a TLS/SSL connection.'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[3])))
                    else:
                        tab.chat_text.setHtml('{0}\n{1} using a <b>TLS/SSL connection</b>.'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[3])))
                except:
                    tab.chat_text.setHtml('{0}\n{1} using a TLS/SSL connection.'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[3])))
                tab.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 318') != -1:
                pass
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 321') != -1:
                pass
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 374') != -1:
                pass
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 322') != -1 or ' '.join(msg_line.split(' ')[0:2]).find(' 353') != -1:
                try:
                    tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                    if settings['Main']['DarkTheme'] == 'Disabled':
                        self.progr.setStyleSheet('background-color: #ffffff; color: #000000;')
                        self.progr.ui.progressBar.setStyleSheet('selection-background-color: #ff7700;')
                    elif settings['Main']['DarkTheme'] == 'Enabled':
                        self.progr.setStyleSheet('background-color: #313131; color: #ffffff;')
                        self.progr.ui.progressBar.setStyleSheet('selection-background-color: rgb(161, 75, 0);')
                    self.progr.ui.value.setText(msg_line.split(' ')[3])
                    if len(self.channels) > 10 and settings['Main']['Language'] == 'English':
                        self.progr.ui.progresstext.setText(en_US.get()['p_chanls'].format(len(self.channels)))
                        self.progr.setWindowTitle(en_US.get()['prgrwait'])
                        self.progr.ui.additional_btn.setText(en_US.get()['addit_bt'])
                        self.progr.ui.propertie.setText(en_US.get()['channelp'])
                    elif len(self.channels) > 10 and settings['Main']['Language'] == 'Russian':
                        self.progr.ui.progresstext.setText(ru_RU.get()['p_chanls'].format(len(self.channels)))
                        self.progr.ui.additional_btn.setText(ru_RU.get()['addit_bt'])
                        self.progr.setWindowTitle(ru_RU.get()['prgrwait'])
                        self.progr.ui.propertie.setText(ru_RU.get()['channelp'])
                    elif len(self.channels) == 10:
                        self.progr.exec_()
                    self.channels.update({msg_line.split(' ')[3]: {'name': msg_line.split(' ')[3], 'topic': " ".join(msg_line.split(' ')[5:]), 'members': int(msg_line.split(' ')[4])}})
                except Exception as e:
                    pass
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 323') != -1:
                try:
                    self.progr.close()
                except:
                    pass
                for channel in self.channels:
                    tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                    try:
                        if settings['Main']['MsgBacklight'] == 'Disabled':
                            tab.chat_text.setHtml('{0}{1}<br>Topic: {2}<br>Members: {3}<br>------------------------------------'.format(tab.chat_text.toHtml(), self.channels[channel]['name'], self.channels[channel]['topic'], self.channels[channel]['members']))
                        else:
                            tab.chat_text.setHtml('{0}<b>{1}</b><br>Topic: {2}<br>Members: {3}<br>-------------------------------------'.format(tab.chat_text.toHtml(), self.channels[channel]['name'], self.channels[channel]['topic'], self.channels[channel]['members']))
                    except:
                        tab.chat_text.setHtml('{0}{1}<br>Topic: {2}<br>Members: {3}<br>------------------------------------'.format(tab.chat_text.toHtml(), self.channels[channel]['name'].replace('<', '&#60;').replace('>', '&#62;'), self.channels[channel]['topic'].replace('<', '&#60;').replace('>', '&#62;'), self.channels[channel]['members']))
                self.channels = {}
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 376') != -1:
                pass
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 378') != -1:
                pass
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 312') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    if settings['Main']['MsgBacklight'] == 'Disabled':
                        tab.chat_text.setHtml('{0}{1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[4:])))
                    else:
                        tab.chat_text.setHtml('{0}{1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[4:])))
                except:
                    tab.chat_text.setHtml('{0}{1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[4:])))
                self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex()).chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 311') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    if settings['Main']['MsgBacklight'] == 'Disabled':
                        tab.chat_text.setHtml('{0}{1} ({2}@{3})<br>Real name: {4}<br>------------------------------------'.format(tab.chat_text.toHtml(), msg_line.split(' ')[3], msg_line.split(' ')[4], msg_line.split(' ')[5], ' '.join(msg_line.split(' ')[7:]).splitlines()[0]))
                    else:
                        tab.chat_text.setHtml('{0}<b>{1}</b> ({2}@{3})<br><i>Real name: {4}</i><br>------------------------------------'.format(tab.chat_text.toHtml(), msg_line.split(' ')[3], msg_line.split(' ')[4], msg_line.split(' ')[5], ' '.join(msg_line.split(' ')[7:]).splitlines()[0]))
                    tab.chat_text.moveCursor(QTextCursor.End)
                except:
                    tab.chat_text.setHtml('{0}{1} ({2}@{3})<br>Real name: {4}<br>------------------------------------'.format(tab.chat_text.toHtml(), msg_line.split(' ')[3], msg_line.split(' ')[4], msg_line.split(' ')[5], ' '.join(msg_line.split(' ')[7:]).splitlines()[0]))
                tab.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 332') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    if settings['Main']['MsgBacklight'] == 'Disabled':
                        tab.chat_text.setHtml('{0}\nTopic: {1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[4:]).replace('http//', 'http://').replace('https//', 'https://').replace('ftp//', 'ftp://')))
                    else:
                        tab.chat_text.setHtml('{0}\n<b>Topic:</b> {1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[4:]).replace('http//', 'http://').replace('https//', 'https://').replace('ftp//', 'ftp://')))
                except:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
                    tab.chat_text.setHtml('{0}\nTopic: {1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[3:]).replace('http//', 'http://').replace('https//', 'https://')))
                tab.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 333') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    if settings['Main']['MsgBacklight'] == 'Disabled':
                        tab.chat_text.setHtml('{0}\nTopic set by {1} ({2})'.format(tab.chat_text.toHtml(), msg_line.split(' ')[4], datetime.datetime.fromtimestamp(int(msg_line.split(' ')[5])).strftime('%Y-%m-%d %H:%M:%S')))
                    else:
                        tab.chat_text.setHtml('{0}\nTopic set by {1} <span style="font-size: 10px">({2})</span>'.format(tab.chat_text.toHtml(), msg_line.split(' ')[4], datetime.datetime.fromtimestamp(int(msg_line.split(' ')[5])).strftime('%Y-%m-%d %H:%M:%S')))
                except:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
                    tab.chat_text.setHtml('{0}\nTopic set by {1} ({2})'.format(tab.chat_text.toHtml(), msg_line.split(' ')[4], datetime.datetime.fromtimestamp(int(msg_line.split(' ')[5])).strftime('%Y-%m-%d %H:%M:%S')))
                tab.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 319') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    if settings['Main']['MsgBacklight'] == 'Disabled':
                        tab.chat_text.setHtml('{0}\nMutual channels: {1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[4:]).replace('@', '').replace('~', '').replace('&', '')))
                    else:
                        tab.chat_text.setHtml('{0}\nMutual channels: {1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[4:]).replace('@', '').replace('~', '').replace('&', '')))
                except:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
                    tab.chat_text.setHtml('{0}\nMutual channels: {1}'.format(tab.chat_text.toHtml(), " ".join(msg_line.split(' ')[4:]).replace('@', '').replace('~', '').replace('&', '')))
                tab.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' 317') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    if settings['Main']['MsgBacklight'] == 'Disabled':
                        tab.chat_text.setHtml('{0}\n{1} idle, last logon time - {2}</span>'.format(tab.chat_text.toHtml(), datetime.datetime.fromtimestamp(int(msg_line.split(' ')[4])).strftime('%H:%M:%S'), datetime.datetime.fromtimestamp(msg_line.split(' ')[5] / 1000).strftime('%Y-%m-%d %H:%M:%S')))
                    else:
                        tab.chat_text.setHtml('{0}\n{1} idle, last logon time - {2}</span>'.format(tab.chat_text.toHtml(), datetime.datetime.fromtimestamp(int(msg_line.split(' ')[4])).strftime('%H:%M:%S'), datetime.datetime.fromtimestamp(int(msg_line.split(' ')[5])).strftime('%Y-%m-%d %H:%M:%S')))
                except:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
                    tab.chat_text.setHtml('{0}\n{1} idle, last logon time - {2}</span>'.format(tab.chat_text.toHtml(), datetime.datetime.fromtimestamp(int(msg_line.split(' ')[4])).strftime('%H:%M:%S'), datetime.datetime.fromtimestamp(int(msg_line.split(' ')[5])).strftime('%Y-%m-%d %H:%M:%S')))
                tab.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find('PRIVMSG') != -1:
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[2] == 'PRIVMSG' and decoded_text[4] == "\001VERSION\001":
                        if platform.system() == "Darwin":
                            self.socket.send(bytes("NOTICE {0} \001VERSION Tinelix IRC Client {1} ({2}). PyQt5 version: {3} | Qt version: {4} | Python version: {5}.{6}.{7} | Platform: {8} | Platform version: {9}\001\r\n".format(decoded_text[0], version, date, PYQT_VERSION_STR, QT_VERSION_STR, sys.version_info[0], sys.version_info[1], sys.version_info[2], platform.system(), " ".join(platform.version().split(" ")[0:2])), self.encoding));
                        else:
                            self.socket.send(bytes("NOTICE {0} \001VERSION Tinelix IRC Client {1} ({2}). PyQt5 version: {3} | Qt version: {4} | Python version: {5}.{6}.{7} | Platform: {8} | Platform version: {9}\001\r\n".format(decoded_text[0], version, date, PYQT_VERSION_STR, QT_VERSION_STR, sys.version_info[0], sys.version_info[1], sys.version_info[2], platform.system(), platform.version()), self.encoding));
                    elif decoded_text[2] == 'PRIVMSG' and decoded_text[4] == "\001CLIENTINFO\001":
                        self.socket.send(bytes("NOTICE {0} \001CLIENTINFO Tinelix IRC Client {1} for Python ({2}). Powered by PyQt5 {3} with Qt {4}. Source code repository link: https://github.com/tinelix/irc-client (GNU GPL 3.0)\001\r\n".format(decoded_text[0], version, date, PYQT_VERSION_STR, QT_VERSION_STR), self.encoding));
                    elif decoded_text[2] == 'PRIVMSG' and decoded_text[4] != "\001VERSION\001" and decoded_text[4] != "\001CLIENTINFO\001":
                        for i in range(self.parent.ui.tabs.count()):
                            if self.parent.ui.tabs.tabText(i) == decoded_text[3]:
                                tab = self.parent.ui.tabs.widget(i)
                                try:
                                    if settings['Main']['MsgBacklight'] == 'Disabled':
                                        tab.chat_text.setHtml('{0}{1}: {2} ({3})'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(decoded_text[4:]).replace('<', '&#60;').replace('>', '&#62;').splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                                    else:
                                        tab.chat_text.setHtml('{0}<b>{1}:</b> {2} <span style="font-size: 10px">({3})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(decoded_text[4:]).replace('<', '&#60;').replace('>', '&#62;').splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")).replace('https//', 'https://').replace('http//', 'http://').replace('ftp//', 'ftp://'))
                                except:
                                    pass
                                if ' '.join(decoded_text[4:]).splitlines()[0].startswith(self.nickname):
                                    mention_notif = MentionNotificationWindow(self)
                                    mention_notif.setWindowFlags(mention_notif.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
                                    mention_notif.setStyleSheet('border-radius: 2px; opacity: 100;')
                                    screen = app.primaryScreen()
                                    size = screen.size()
                                    mention_notif.setGeometry(size.width() - 400, size.height() - 180, 313, 128)
                                    try:
                                        if settings['Main']['Language'] == 'English':
                                            mention_notif.ui.nickname_label.setText(en_US.get()['mentionl'].format(decoded_text[0]))
                                            mention_notif.ui.openclient_btn.setText(en_US.get()['opclient'])
                                        else:
                                            mention_notif.ui.nickname_label.setText(ru_RU.get()['mentionl'].format(decoded_text[0]))
                                        mention_notif.ui.openclient_btn.setText(ru_RU.get()['opclient'])
                                    except:
                                        pass
                                    mention_notif.ui.msg_text.setText(' '.join(decoded_text[4:]).splitlines()[0])
                                    mention_notif.show()
                                tab.chat_text.moveCursor(QTextCursor.End)
                except Exception as e:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
                    self.parent.child_widget.chat_text.setHtml('{0}<br>{1}'.format(self.parent.child_widget.chat_text.toHtml(), msg_line))
                    self.parent.child_widget.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find('NOTICE') != -1:
                decoded_text = status.replace('!', ' ').split(' ')
                try:
                    if decoded_text[2] == 'NOTICE' and decoded_text[4] == "\001VERSION":
                        tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                        if settings['Main']['MsgBacklight'] == 'Disabled':
                            tab.chat_text.setHtml('{0}\n{1}: {2} (CTCP | {3})'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(decoded_text[5:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        else:
                            tab.chat_text.setHtml('{0}\n<b>{1}:</b> {2} <span style="font-size: 10px">(CTCP-VERSION | {3})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(decoded_text[5:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        self.parent.child_widget.chat_text.moveCursor(QTextCursor.End)
                    elif decoded_text[2] == 'NOTICE' and decoded_text[4] == "\001CLIENTINFO":
                        tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                        if settings['Main']['MsgBacklight'] == 'Disabled':
                            tab.chat_text.setHtml('{0}\n{1}: {2} (CTCP-CLIENTINFO | {3})'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(decoded_text[5:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        else:
                            tab.chat_text.setHtml('{0}\n<b>{1}:</b> {2} <span style="font-size: 10px">(CTCP-CLIENTINFO | {3})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(decoded_text[5:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                    elif decoded_text[2] == 'NOTICE':
                        tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                        if settings['Main']['MsgBacklight'] == 'Disabled':
                            tab.chat_text.setHtml('{0}\n{1} sent a notification: {2} ({3})'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(decoded_text[4:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        else:
                            tab.chat_text.setHtml('{0}\n<b>{1}</b> sent a notification: {2} <span style="font-size: 10px">({3})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(decoded_text[4:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                    self.parent.child_widget.chat_text.moveCursor(QTextCursor.End)
                except Exception as e:
                        exc_type, exc_value, exc_tb = sys.exc_info()
                        ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                        print("\n".join(ex))
                        self.parent.child_widget.chat_text.setHtml('{0}\n{1}'.format(self.parent.child_widget.chat_text.toHtml(), msg_line))
                        self.parent.child_widget.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find('MODE') != -1:
                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[2] == 'MODE':
                        tab.chat_text.setHtml('{0}\nEnabled user modes for {1}: {2} ({3})'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(decoded_text[3:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                        self.parent.child_widget.chat_text.moveCursor(QTextCursor.End)
                except Exception as e:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
                    self.parent.child_widget.chat_text.setHtml('{0}\n{1}'.format(self.parent.child_widget.chat_text.toHtml(), msg_line))
                    self.parent.child_widget.chat_text.moveCursor(QTextCursor.End)
            elif ' '.join(msg_line.split(' ')[0:2]).find(' JOIN') != -1:
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[2] == 'JOIN':
                        for i in range(self.parent.ui.tabs.count()):
                            if self.parent.ui.tabs.tabText(i) == decoded_text[3].splitlines()[0]:
                                tab = self.parent.ui.tabs.widget(i)
                                try:
                                    if settings['Main']['MsgBacklight'] == 'Disabled':
                                        tab.chat_text.setHtml('{0}\n{1} joined on the channel {2}. ({3})'.format(tab.chat_text.toHtml(), decoded_text[0], " ".join(decoded_text[3:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                                    else:
                                        tab.chat_text.setHtml('{0}<b>{1}</b> joined on the channel {2}. <span style="font-size: 10px">({3})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], " ".join(decoded_text[3:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                                except:
                                    exc_type, exc_value, exc_tb = sys.exc_info()
                                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                                    print("\n".join(ex))
                                tab.chat_text.moveCursor(QTextCursor.End)
                                self.socket.send(bytes('NAMES {0}\r\n'.format(self.parent.ui.tabs.tabText(i)), self.encoding))
                        try:
                            if settings['Main']['Language'] == 'English':
                                self.parent.ui.status_label.setText(en_US.get()['chstatus'].format(''.join(decoded_text[3].splitlines()[0])))
                            else:
                                self.parent.ui.status_label.setText(ru_RU.get()['chstatus'].format(''.join(decoded_text[3].splitlines()[0])))
                        except:
                            exc_type, exc_value, exc_tb = sys.exc_info()
                            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                            print("\n".join(ex))
                except:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
            elif ' '.join(msg_line.split(' ')[0:2]).find(' PART') != -1:
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[0] == self.nickname:
                        pass
                    elif decoded_text[2] == 'PART':
                        for i in range(self.parent.ui.tabs.count()):
                            if self.parent.ui.tabs.tabText(i) == decoded_text[3].splitlines()[0]:
                                tab = self.parent.ui.tabs.widget(i)
                                reason = []
                                try:
                                    for word in msg_line.split(' '):
                                        if msg_line.split(' ').index(word) > 2 and word != '':
                                            reason.append(word.splitlines()[0])
                                    if settings['Main']['MsgBacklight'] == 'Disabled' and reason != []:
                                        tab.chat_text.setHtml('{0}\n{1} left the {2} channel with reason: {3}. ({4})'.format(tab.chat_text.toHtml(), decoded_text[0], decoded_text[3], ' '.join(reason).replace('<', '&#60;').replace('>', '&#62;'), datetime.datetime.now().strftime("%H:%M:%S")))
                                    elif settings['Main']['MsgBacklight'] == 'Enabled' and reason != []:
                                        tab.chat_text.setHtml('{0}<b>{1}</b> left the {2} channel with reason: <i>{3}</i>. <span style="font-size: 10px">({4})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], decoded_text[3], ' '.join(reason).replace('<', '&#60;').replace('>', '&#62;'), datetime.datetime.now().strftime("%H:%M:%S")))
                                    elif settings['Main']['MsgBacklight'] == 'Enabled':
                                        tab.chat_text.setHtml('{0}<b>{1}</b> left the {2} channel. <span style="font-size: 10px">({3})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], decoded_text[3], datetime.datetime.now().strftime("%H:%M:%S")))
                                    else:
                                        tab.chat_text.setHtml('{0}\n{1} left the {2} channel. ({3})'.format(tab.chat_text.toHtml(), decoded_text[0], decoded_text[3], datetime.datetime.now().strftime("%H:%M:%S")))
                                except Exception as e:
                                    tab.chat_text.setHtml('{0}\n{1} left the {2} channel. ({3})'.format(tab.chat_text.toHtml(), decoded_text[0], decoded_text[3], datetime.datetime.now().strftime("%H:%M:%S")))
                                tab.chat_text.moveCursor(QTextCursor.End)
                                self.socket.send(bytes('NAMES {0}\r\n'.format(self.parent.ui.tabs.tabText(i)), self.encoding))
                        try:
                            if settings['Main']['Language'] == 'English':
                                self.parent.ui.status_label.setText(en_US.get()['chstatus'].format(''.join(decoded_text[3].splitlines()[0])))
                            else:
                                self.parent.ui.status_label.setText(ru_RU.get()['chstatus'].format(''.join(decoded_text[3].splitlines()[0])))
                        except:
                            pass
                except Exception as e:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                    print("\n".join(ex))
                    self.parent.child_widget.chat_text.setHtml('{0}<br>{1}'.format(self.parent.child_widget.chat_text.toHtml(), msg_line))
                    self.parent.child_widget.chat_text.moveCursor(QTextCursor.End)
            elif msg_line.find(' QUIT') != -1:
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[2] == 'QUIT':
                        for i in range(self.parent.ui.tabs.count()):
                            if self.parent.ui.tabs.tabText(i) == self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()):
                                tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                                reason = []
                                try:
                                    for word in msg_line.split(' '):
                                        if msg_line.split(' ').index(word) > 1 and word != '':
                                            reason.append(word.splitlines()[0])
                                    if settings['Main']['MsgBacklight'] == 'Disabled' and reason != []:
                                        tab.chat_text.setHtml('{0}\n{1} quited with reason: {2}. ({3})'.format(tab.chat_text.toHtml(), decoded_text[0], " ".join(reason), datetime.datetime.now().strftime("%H:%M:%S")))
                                    elif settings['Main']['MsgBacklight'] == 'Enabled' and reason != []:
                                        tab.chat_text.setHtml('{0}<b>{1}</b> quited with reason: <i>{2}</i>. <span style="font-size: 10px">({3})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], ' '.join(reason).replace('<', '&#60;').replace('>', '&#62;'), datetime.datetime.now().strftime("%H:%M:%S")))
                                    elif settings['Main']['MsgBacklight'] == 'Enabled':
                                        tab.chat_text.setHtml('{0}<b>{1}</b> quited. <span style="font-size: 10px">({2})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], datetime.datetime.now().strftime("%H:%M:%S")))
                                    else:
                                        tab.chat_text.setHtml('{0}\n{1} quited. <span style="font-size: 10px">({2})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], datetime.datetime.now().strftime("%H:%M:%S")))
                                except Exception as e:
                                    exc_type, exc_value, exc_tb = sys.exc_info()
                                    ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                                    print("\n".join(ex))
                                    tab.chat_text.setHtml('{0}\n{1} quited. <span style="font-size: 10px">({2})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], datetime.datetime.now().strftime("%H:%M:%S")))
                                tab.chat_text.moveCursor(QTextCursor.End)
                                self.socket.send(bytes('NAMES {0}\r\n'.format(self.parent.ui.tabs.tabText(i)), self.encoding))
                        if settings['Main']['Language'] == 'English':
                            self.parent.ui.status_label.setText(en_US.get()['rdstatus'])
                        else:
                            self.parent.ui.status_label.setText(ru_RU.get()['rdstatus'])
                except Exception as e:
                    print(e)
                    self.parent.child_widget.chat_text.setHtml('{0}\n{1}'.format(self.parent.child_widget.chat_text.toHtml(), msg_line))
                    self.parent.child_widget.chat_text.moveCursor(QTextCursor.End)
            elif msg_line.find(' NICK') != -1:
                try:
                    decoded_text = status.replace('!', ' ').split(' ')
                    if decoded_text[2] == 'NICK':
                        for i in range(self.parent.ui.tabs.count()):
                            if self.parent.ui.tabs.tabText(i) == self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()):
                                try:
                                    tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                                    if settings['Main']['MsgBacklight'] == 'Disabled':
                                        tab.chat_text.setHtml('{0}\n{1} changed nickname to {2}. ({3})'.format(tab.chat_text.toHtml(), decoded_text[0], " ".join(decoded_text[3:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                                    else:
                                        tab.chat_text.setHtml('{0}<b>{1}</b> changed nickname to {2}. <span style="font-size: 10px">({3})</span>'.format(tab.chat_text.toHtml(), decoded_text[0], " ".join(decoded_text[3:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                                except:
                                    tab.chat_text.setHtml('{0}\n{1} changed nickname to {2}. ({3})'.format(tab.chat_text.toHtml(), decoded_text[0], " ".join(decoded_text[3:]).splitlines()[0], datetime.datetime.now().strftime("%H:%M:%S")))
                                tab.chat_text.moveCursor(QTextCursor.End)
                                self.socket.send(bytes('NAMES {0}\r\n'.format(self.parent.ui.tabs.tabText(i)), self.encoding))
                        try:
                            if settings['Main']['Language'] == 'English':
                                self.parent.ui.status_label.setText(en_US.get()['rdstatus'])
                            else:
                                self.parent.ui.status_label.setText(ru_RU.get()['rdstatus'])
                        except:
                            pass
                except:
                    if self.channels == {} and self.owners == [] and self.operators == [] and self.members == []:
                        self.parent.child_widget.chat_text.setHtml('{0}\n{1}'.format(self.parent.child_widget.chat_text.toHtml(), msg_line))
                    self.parent.child_widget.chat_text.moveCursor(QTextCursor.End)
            elif msg_line.startswith('Exception: '):
                self.parent.child_widget.chat_text.setHtml('{0}'.format(msg_line))
                self.socket.close()
                self.thread.stop()
                if msg_line.startswith('Exception: [Errno 60]') or msg_line.startswith('Exception: [Errno -3]') or msg_line.startswith('Exception: [Errno 110]'):
                    self.timer = QTimer()
                    self.timer.timeout.connect(self.irc_reconnect)
                    self.timer.start(5000)
                    self.timer_2 = QTimer()
                    self.timer_2.timeout.connect(self.irc_reconnect_msg)
                    self.timer_2.start(4000)
                else:
                    self.ui.connect_btn.clicked.disconnect()
                    self.ui.connect_btn.clicked.connect(self.irc_connect)
                if settings.sections() != [] and settings['Main']['Language'] == 'Russian':
                    self.ui.connect_btn.setText(ru_RU.get()['conn_btn'])
                elif settings.sections() != [] and settings['Main']['Language'] == 'English':
                    self.ui.connect_btn.setText(en_US.get()['conn_btn'])
            else:
                for i in range(self.parent.ui.tabs.count()):
                    if self.parent.ui.tabs.tabText(i) == self.parent.ui.tabs.tabText(self.parent.ui.tabs.currentIndex()):
                        tab = self.parent.ui.tabs.widget(self.parent.ui.tabs.currentIndex())
                        message_code = []
                        message_splited = []
                        for string in msg_line.split(' '):
                            if msg_line.split(' ').index(string) == 1 and string.isdigit() == True:
                                message_code.append(int(string))
                            if msg_line.index(string) > 1 and message_code != []:
                                message_splited.append(string.splitlines()[0])
                        if message_code != [] and (self.channels == {} and self.owners == [] and self.operators == [] and self.members == []):
                            tab.chat_text.setHtml('{0}\nCode {1:03d}: {2}'.format(tab.chat_text.toHtml(), message_code[0], ' '.join(message_splited[2:]).replace('<', '&#60;').replace('>', '&#62;')))
                        elif (self.channels == {} and self.owners == [] and self.operators == [] and self.members == []):
                            tab.chat_text.setHtml('{0}\n{1}'.format(tab.chat_text.toHtml(), msg_line))
                        tab.chat_text.moveCursor(QTextCursor.End)
            try:
                if not msg_line.startswith('Exception: ') and settings.sections() != [] and settings['Main']['MsgHistory'] == 'Enabled':
                    if not os.path.exists('history'):
                        os.makedirs('history')
                        for i in range(self.parent.ui.tabs.count()):
                            with open('history/irc_{0}_{1}_{2}.html'.format(self.parent.ui.tabs.tabText(i), self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text(), self.now.strftime('%Y-%m-%d_%H.%M.%S')), 'w+') as f:
                                if settings['Main']['Language'] == 'Russian':
                                    f.write("<!DOCTYPE HTML>\n<html>\n<head>\n<link href=\"https://fonts.googleapis.com/css?family=Roboto:400,100,100italic,300,300italic,400italic,500,500italic,700,700italic,900italic,900\" rel=\"stylesheet\">\n<title>История сообщений</title>\n<style>\nbody |(\nfont-family: \"Roboto\", \"Arial\";\nmargin: 12px;\n|);\n</style>\n</head>\n<body>\n<h3 style=\"margin-top: 12px; margin-bottom: 0px;\">История сообщений</h3><i style=\"font-size: 12px; color: #6a6a6a;\">{0} • {1} • {2}</i>\n<p><div style=\"font-family: {3}, Courier New; border-radius: 8px; background-color: #ededed; padding: 10px; border-radius: 8px;\">\n{4}\n</div>\n</body>\n</html>".format(self.now.strftime('%Y-%m-%d %H:%M:%S'), str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()), self.parent.ui.tabs.tabText(i), settings['Main']['MsgFont'].split(", ")[0], self.parent.ui.tabs.widget(i).chat_text.toPlainText().replace("\n", "<br>")).replace("|(", "{").replace("|)", "}"));
                                else:
                                    f.write("<!DOCTYPE HTML>\n<html>\n<head>\n<link href=\"https://fonts.googleapis.com/css?family=Roboto:400,100,100italic,300,300italic,400italic,500,500italic,700,700italic,900italic,900\" rel=\"stylesheet\">\n<title>Messages history</title>\n<style>\nbody |(\nfont-family: \"Roboto\", \"Arial\";\nmargin: 12px;\n|);\n</style>\n</head>\n<body>\n<h3 style=\"margin-top: 12px; margin-bottom: 0px;\">Messages history</h3><i style=\"font-size: 12px; color: #6a6a6a;\">{0} • {1} • {2}</i>\n<p><div style=\"font-family: {3}, Courier New; border-radius: 8px; background-color: #ededed; padding: 10px; border-radius: 8px;\">\n{4}\n</div>\n</body>\n</html>".format(self.now.strftime('%Y-%m-%d %H:%M:%S'), str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()), self.parent.ui.tabs.tabText(i), settings['Main']['MsgFont'].split(", ")[0], self.parent.ui.tabs.widget(i).chat_text.toPlainText().replace("\n", "<br>")).replace("|(", "{").replace("|)", "}"));
                        self.parent.ui.msg_history.triggered.disconnect()
                        self.parent.ui.msg_history.triggered.connect(self.show_channel_history)
                    else:
                        for i in range(self.parent.ui.tabs.count()):
                            with open('history/irc_{0}_{1}_{2}.html'.format(self.parent.ui.tabs.tabText(i), str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()), self.now.strftime('%Y-%m-%d_%H.%M.%S')), 'w+') as f:
                                if settings['Main']['Language'] == 'Russian':
                                    f.write("<!DOCTYPE HTML>\n<html>\n<head>\n<link href=\"https://fonts.googleapis.com/css?family=Roboto:400,100,100italic,300,300italic,400italic,500,500italic,700,700italic,900italic,900\" rel=\"stylesheet\">\n<title>История сообщений</title>\n<style>\nbody |(\nfont-family: \"Roboto\", \"Arial\";\nmargin: 12px;\n|);\n</style>\n</head>\n<body>\n<h3 style=\"margin-top: 12px; margin-bottom: 0px;\">История сообщений</h3><i style=\"font-size: 12px; color: #6a6a6a;\">{0} • {1} • {2}</i>\n<p><div style=\"font-family: {3}, Courier New; border-radius: 8px; background-color: #ededed; padding: 10px; border-radius: 8px;\">\n{4}\n</div>\n</body>\n</html>".format(self.now.strftime('%Y-%m-%d %H:%M:%S'), str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()), self.parent.ui.tabs.tabText(i), settings['Main']['MsgFont'].split(", ")[0], self.parent.ui.tabs.widget(i).chat_text.toPlainText().replace("\n", "<br>")).replace("|(", "{").replace("|)", "}"));
                                else:
                                    f.write("<!DOCTYPE HTML>\n<html>\n<head>\n<link href=\"https://fonts.googleapis.com/css?family=Roboto:400,100,100italic,300,300italic,400italic,500,500italic,700,700italic,900italic,900\" rel=\"stylesheet\">\n<title>Messages history</title>\n<style>\nbody |(\nfont-family: \"Roboto\", \"Arial\";\nmargin: 12px;\n|);\n</style>\n</head>\n<body>\n<h3 style=\"margin-top: 12px; margin-bottom: 0px;\">Messages history</h3><i style=\"font-size: 12px; color: #6a6a6a;\">{0} • {1} • {2}</i>\n<p><div style=\"font-family: {3}, Courier New; border-radius: 8px; background-color: #ededed; padding: 10px; border-radius: 8px;\">\n{4}\n</div>\n</body>\n</html>".format(self.now.strftime('%Y-%m-%d %H:%M:%S'), str(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()), self.parent.ui.tabs.tabText(i), settings['Main']['MsgFont'].split(", ")[0], self.parent.ui.tabs.widget(i).chat_text.toPlainText().replace("\n", "<br>")).replace("|(", "{").replace("|)", "}"));
                        self.parent.ui.msg_history.triggered.disconnect()
                        self.parent.ui.msg_history.triggered.connect(self.show_channel_history)
            except:
                exc_type, exc_value, exc_tb = sys.exc_info()
                ex = traceback.format_exception(exc_type, exc_value, exc_tb)
                print("\n".join(ex))

