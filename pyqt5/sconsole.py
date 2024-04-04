def change_theme(self):
        if self.child_5.ui.dark_theme_cb.checkState() == False:
            self.child_5.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            self.child_5.ui.language_combo.setStyleSheet('selection-background-color: #ff7700')
            self.child_5.ui.msgfont_combo.setStyleSheet('selection-background-color: #ff7700')
            self.ui.line.setStyleSheet('color: #afafaf')
            self.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
            self.ui.menubar.setStyleSheet('selection-background-color: #ff7700; selection-color: #000000')
            self.ui.conn_quality_progr.setStyleSheet('selection-background-color: #ff7700')
            for i in range(self.ui.tabs.count()):
                tab = self.ui.tabs.widget(i)
                tab.setStyleSheet('background-color: #ffffff;\ncolor: #000000;')
                tab.chat_text.setStyleSheet('selection-background-color: #ff7700')
                tab.members_list.setStyleSheet('selection-background-color: #ff7700')
                tab.verticalScrollBar.setStyleSheet('QScrollBar:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: #ff7700;\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_light.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_light.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
                tab.verticalScrollBar_2.setStyleSheet('QScrollBar:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: #ff7700;\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_light.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(255, 255, 255);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_light.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
            if self.child_widget.message_text.isEnabled() == True:
                self.child_widget.message_text.setStyleSheet('selection-background-color: #ff7700')
            else:
                self.child_widget.message_text.setStyleSheet('selection-background-color: #ff7700; color: #4f4f4f')
                self.child_widget.send_msg_btn.setEnabled(False)
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
            self.child_5.ui.language_combo.setStyleSheet('selection-background-color: #a14b00')
            self.child_5.ui.msgfont_combo.setStyleSheet('selection-background-color: #a14b00')
            self.ui.line.setStyleSheet('color: #4a4a4a')
            self.child.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            self.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
            self.ui.menubar.setStyleSheet('selection-background-color: #a14b00; selection-color: #ffffff')
            self.ui.conn_quality_progr.setStyleSheet('selection-background-color: #a14b00')
            for i in range(self.ui.tabs.count()):
                tab = self.ui.tabs.widget(i)
                tab.setStyleSheet('background-color: #313131;\ncolor: #ffffff;')
                tab.chat_text.setStyleSheet('selection-background-color: #a14b00')
                tab.members_list.setStyleSheet('selection-background-color: #a14b00')
                tab.verticalScrollBar.setStyleSheet('QScrollBar:vertical {border: 0px solid;\nbackground: rgb(43, 43, 43);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: rgb(161, 75, 0);\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_dark.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_dark.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
                tab.verticalScrollBar_2.setStyleSheet('QScrollBar:vertical {border: 0px solid;\nbackground: rgb(43, 43, 43);\nwidth: 15px;\nmargin: 16px 0 16px 0;\n}\nQScrollBar::handle:vertical {\nbackground: rgb(161, 75, 0);\nborder-width: 2px;\nborder-radius: 10px;\n}\n\nQScrollBar::add-line:vertical {\nborder: 0px solid;\nbackground-color: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: bottom;\nsubcontrol-origin: margin;\nimage: url(:/arrows/up_arrow_dark.png);\n}\n\nQScrollBar::sub-line:vertical {\nborder: 0px solid;\nbackground: rgb(43, 43, 43);\nheight: 16px;\nsubcontrol-position: top;\nsubcontrol-origin: margin;\nimage: url(:/arrows/down_arrow_dark.png);\n}\n\nQScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\nbackground: none;\n}')
            if self.child_widget.message_text.isEnabled() == True:
                self.child_widget.message_text.setStyleSheet('selection-background-color: #a14b00')
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


def save_settings(self, settings, QFont, translator, sys, traceback, en_US, ru_RU):
        try:
            settings.read('settings')
            settings['Main']['Language'] = self.child_5.ui.language_combo.currentText()
            if self.child_5.ui.dark_theme_cb.checkState() == 0:
                settings['Main']['DarkTheme'] = 'Disabled'
            else:
                settings['Main']['DarkTheme'] = 'Enabled'

            if self.child_5.ui.msgs_hint.checkState() == 0:
                settings['Main']['MessagesHint'] = 'Disabled'
            else:
                settings['Main']['MessagesHint'] = 'Enabled'

            if self.child_5.ui.save_msghistory_cb.checkState() == 0:
                settings['Main']['MsgHistory'] = 'Disabled'
            else:
                settings['Main']['MsgHistory'] = 'Enabled'
            if self.child_5.ui.backlight_cb.checkState() == 0:
                settings['Main']['MsgBacklight'] = 'Disabled'
            else:
                settings['Main']['MsgBacklight'] = 'Enabled'
            font = '{0}, {1}'.format(QFont(self.child_5.ui.msgfont_combo.currentFont()).family(), self.child_5.ui.font_size_sb.value())
            settings['Main']['MsgFont'] = font
            if self.child_5.ui.parsing_debugger_cb.checkState() == 0:
                settings['Main']['ParsingDebugger'] = 'Disabled'
            else:
                settings['Main']['ParsingDebugger'] = 'Enabled'
            with open('settings', 'w+') as configfile:
                settings.write(configfile)
            translator.translate_001(self, self.child.ui, settings['Main']['Language'], en_US, ru_RU)
            font = QFont(settings['Main']['MsgFont'].split(', ')[0])
            try:
                font.setPointSize(int(settings['Main']['MsgFont'].split(', ')[1]))
            except:
                pass
            for i in range(self.ui.tabs.count()):
                self.ui.tabs.widget(i).chat_text.setFont(font)
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
            print("\n".join(ex))

def change_language(self, settings, translator, sys, traceback):
        index = self.child.ui.language_combo.currentIndex()
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
            exc_type, exc_value, exc_tb = sys.exc_info()
            ex = traceback.format_exception(exc_type, exc_value, exc_tb)
            print("\n".join(ex))
