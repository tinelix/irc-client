from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR

def translate_001(mainclass, form, language, en_US, ru_RU):
    if language == 'Russian':
        try:
            form.title_label.setText(ru_RU.get()['1stsetup'])
            form.profiles_name.setText(ru_RU.get()['profiles'])
            form.tableWidget.horizontalHeaderItem(0).setText(ru_RU.get()['profile'])
            form.tableWidget.horizontalHeaderItem(1).setText(ru_RU.get()['servport'])
            form.add_profile_btn.setText(ru_RU.get()['add_btn'])
            form.connect_btn.setText(ru_RU.get()['conn_btn'])
            form.change_profile_btn.setText(ru_RU.get()['chpf_btn'])
            form.del_profile_btn.setText(ru_RU.get()['del_btn'])
        except:
            pass
        try:
            mainclass.ui.menu.setTitle(ru_RU.get()['filemenu'])
            mainclass.ui.menu_4.setTitle(ru_RU.get()['chanmenu'])
            mainclass.ui.menu_2.setTitle(ru_RU.get()['helpmenu'])
            mainclass.ui.menu_3.setTitle(ru_RU.get()['viewmenu'])
            mainclass.ui.connect_item.setText(ru_RU.get()['conn_mi'])
            mainclass.ui.settings_item.setText(ru_RU.get()['setsitem'])
            mainclass.ui.quit_item.setText(ru_RU.get()['quit_mi'])
            mainclass.ui.about_item.setText(ru_RU.get()['about_mi'])
            mainclass.ui.join_item.setText(ru_RU.get()['joinchan'])
            mainclass.ui.leave_item.setText(ru_RU.get()['lv_chan'])
            mainclass.ui.msg_history.setText(ru_RU.get()['msg_hist'])
            mainclass.child_widget.send_msg_btn.setText(ru_RU.get()['send_msg'])
            if mainclass.child_widget.message_text.isEnabled() == False:
                mainclass.child_widget.message_text.setText(ru_RU.get()['cantsmsg'])
            mainclass.ui.conn_quality_label.setText(ru_RU.get()['connqual'])
            mainclass.child_widget.error_getting_member_list.setText(ru_RU.get()['mbgt_err'])
            mainclass.child_widget.close_panel_btn.setText(ru_RU.get()['mbget_cl'])
        except Exception as e:
            print(e)
    elif language == 'English':
        try:
            mainclass.ui.menu.setTitle(en_US.get()['filemenu'])
            mainclass.ui.menu_4.setTitle(en_US.get()['chanmenu'])
            mainclass.ui.menu_2.setTitle(en_US.get()['helpmenu'])
            mainclass.ui.menu_3.setTitle(en_US.get()['viewmenu'])
            mainclass.ui.connect_item.setText(en_US.get()['conn_mi'])
            mainclass.ui.settings_item.setText(en_US.get()['setsitem'])
            mainclass.ui.quit_item.setText(en_US.get()['quit_mi'])
            mainclass.ui.about_item.setText(en_US.get()['about_mi'])
            mainclass.ui.join_item.setText(en_US.get()['joinchan'])
            mainclass.ui.leave_item.setText(en_US.get()['lv_chan'])
            mainclass.ui.msg_history.setText(en_US.get()['msg_hist'])
            mainclass.child_widget.send_msg_btn.setText(en_US.get()['send_msg'])
            if mainclass.child_widget.message_text.isEnabled() == False:
                mainclass.child_widget.message_text.setText(en_US.get()['cantsmsg'])
            mainclass.ui.conn_quality_label.setText(en_US.get()['connqual'])
            mainclass.child_widget.error_getting_member_list.setText(en_US.get()['mbgt_err'])
            mainclass.child_widget.close_panel_btn.setText(en_US.get()['mbget_cl'])
        except Exception as e:
            print(e)
        try:
            form.title_label.setText(en_US.get()['1stsetup'])
            form.profiles_name.setText(en_US.get()['profiles'])
            form.tableWidget.horizontalHeaderItem(0).setText(en_US.get()['profile'])
            form.tableWidget.horizontalHeaderItem(1).setText(en_US.get()['servport'])
            form.add_profile_btn.setText(en_US.get()['add_btn'])
            form.connect_btn.setText(en_US.get()['conn_btn'])
            form.change_profile_btn.setText(en_US.get()['chpf_btn'])
            form.del_profile_btn.setText(en_US.get()['del_btn'])
        except:
            pass

def translate_003(mainclass, form, language, en_US, ru_RU):
    if language == 'Russian':
        try:
            form.tabWidget.setTabText(0, ru_RU.get()['main_tab'])
            form.tabWidget.setTabText(1, ru_RU.get()['conn_tab'])
            form.tabWidget.setTabText(2, ru_RU.get()['identtab'])
            form.profname_label.setText(ru_RU.get()['chprofnm'])
            form.authm_label.setText(ru_RU.get()['authmeth'])
            form.nicknames_label.setText(ru_RU.get()['nicklist'])
            form.password_label.setText(ru_RU.get()['password'])
            form.realname_label.setText(ru_RU.get()['realname'])
            form.hostname_label.setText(ru_RU.get()['hostname'])
            form.server_label.setText(ru_RU.get()['server'])
            form.port_label.setText(ru_RU.get()['port'])
            form.encoding_label.setText(ru_RU.get()['encoding'])
            form.quitmsg_label.setText(ru_RU.get()['quit_msg'])
            form.requiredssl_cb.setText(ru_RU.get()['only_ssl'])
        except Exception as e:
            print(e)
    elif language == 'English':
        try:
            form.tabWidget.setTabText(0, en_US.get()['main_tab'])
            form.tabWidget.setTabText(1, en_US.get()['conn_tab'])
            form.tabWidget.setTabText(2, en_US.get()['identtab'])
            form.profname_label.setText(en_US.get()['chprofnm'])
            form.authm_label.setText(en_US.get()['authmeth'])
            form.nicknames_label.setText(en_US.get()['nicklist'])
            form.password_label.setText(en_US.get()['password'])
            form.realname_label.setText(en_US.get()['realname'])
            form.hostname_label.setText(en_US.get()['hostname'])
            form.server_label.setText(en_US.get()['server'])
            form.port_label.setText(en_US.get()['port'])
            form.encoding_label.setText(en_US.get()['encoding'])
            form.quitmsg_label.setText(en_US.get()['quit_msg'])
            form.requiredssl_cb.setText(en_US.get()['only_ssl'])
        except Exception as e:
            print(e)


def translate_004(mainclass, form, language, en_US, ru_RU):
    form.progname.setText(en_US.get()['prog_ver'].format(mainclass.version))
    if language == 'Russian':
        try:
            mainclass.child_4.setWindowTitle(ru_RU.get()['about_tt'])
            form.about_used_components.setTitle(ru_RU.get()['usingcmp'])
            form.pyqt_version_label.setText(ru_RU.get()['pyqt_ver'])
            form.qt_version_label.setText(ru_RU.get()['qt_fwver'])
            form.python_version_label.setText(ru_RU.get()['python_v'])
            form.about_software_platform.setTitle(ru_RU.get()['about_sys'])
            form.platform_label.setText(ru_RU.get()['platform'])
            form.platform_version_label.setText(ru_RU.get()['ptfm_ver'])
            form.label.setText(ru_RU.get()['gpl_info'])
            form.repo_btn.setText(ru_RU.get()['repo_btn'])
            form.website_btn.setText(ru_RU.get()['webs_btn'])
        except Exception as e:
            pass
    elif language == 'English':
        try:
            mainclass.child_4.setWindowTitle(en_US.get()['about_tt'])
            form.about_used_components.setTitle(en_US.get()['usingcmp'])
            form.pyqt_version_label.setText(en_US.get()['pyqt_ver'])
            form.qt_version_label.setText(en_US.get()['qt_fwver'])
            form.python_version_label.setText(en_US.get()['python_v'])
            form.about_software_platform.setTitle(en_US.get()['aboutsys'])
            form.platform_label.setText(en_US.get()['platform'])
            form.platform_version_label.setText(en_US.get()['ptfm_ver'])
            form.label.setText(en_US.get()['gpl_info'])
            form.repo_btn.setText(en_US.get()['repo_btn'])
            form.website_btn.setText(en_US.get()['webs_btn'])
        except Exception as e:
            print(e)

def translate_005(mainclass, form, language, en_US, ru_RU):
    if language == 'Russian':
        try:
            mainclass.child_5.setWindowTitle(ru_RU.get()['setsitem'])
            form.title_label.setText((ru_RU.get()['setsitem']))
            form.dark_theme_cb.setText(ru_RU.get()['darkthcb'])
            form.save_msghistory_cb.setText(ru_RU.get()['msghstcb'])
            form.msgs_hint.setText(ru_RU.get()['msgshtcb'])
            form.msgs_hint.setText(ru_RU.get()['msgshtcb'])
            form.msgs_hint.setText(ru_RU.get()['msgshtcb'])
            form.backlight_cb.setText(ru_RU.get()['msgbclcb'])
            form.font_label.setText(ru_RU.get()['msg_font'])
            form.parsing_debugger_cb.setText(ru_RU.get()['parsdbg'])
        except Exception as e:
            print(e)
    elif language == 'English':
        try:
            mainclass.child_5.setWindowTitle(en_US.get()['setsitem'])
            form.title_label.setText((en_US.get()['setsitem']))
            form.dark_theme_cb.setText(en_US.get()['darkthcb'])
            form.save_msghistory_cb.setText(en_US.get()['msghstcb'])
            form.msgs_hint.setText(en_US.get()['msgshtcb'])
            form.backlight_cb.setText(en_US.get()['msgbclcb'])
            form.font_label.setText(en_US.get()['msg_font'])
            form.parsing_debugger_cb.setText(en_US.get()['parsdbg'])
        except Exception as e:
            print(e)

