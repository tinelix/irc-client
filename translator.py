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
            mainclass.ui.menu_2.setTitle(ru_RU.get()['helpmenu'])
            mainclass.ui.connect_item.setText(ru_RU.get()['conn_mi'])
            mainclass.ui.quit_item.setText(ru_RU.get()['quit_mi'])
            mainclass.ui.about_item.setText(ru_RU.get()['about_mi'])
        except:
            pass
    elif language == 'English':
        try:
            mainclass.ui.menu.setTitle(en_US.get()['filemenu'])
            mainclass.ui.menu_2.setTitle(en_US.get()['helpmenu'])
            mainclass.ui.connect_item.setText(en_US.get()['conn_mi'])
            mainclass.ui.quit_item.setText(en_US.get()['quit_mi'])
            mainclass.ui.about_item.setText(en_US.get()['about_mi'])
        except:
            pass
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
            form.server_label.setText(ru_RU.get()['server'])
            form.port_label.setText(ru_RU.get()['port'])
            form.encoding_label.setText(ru_RU.get()['encoding'])
            form.quitmsg_label.setText(ru_RU.get()['quit_msg'])
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
            form.server_label.setText(en_US.get()['server'])
            form.port_label.setText(en_US.get()['port'])
            form.encoding_label.setText(en_US.get()['encoding'])
            form.quitmsg_label.setText(en_US.get()['quit_msg'])
        except Exception as e:
            print(e)


def translate_004(mainclass, form, language, en_US, ru_RU):
    form.progname.setText(en_US.get()['prog_ver'].format(mainclass.version))
    if language == 'Russian':
        try:
            mainclass.setWindowTitle(ru_RU.get()['about_tt'])
            form.description_label.setText(ru_RU.get()['free_sft'].format(QT_VERSION_STR, PYQT_VERSION_STR))
            form.label.setText(ru_RU.get()['gpl_info'])
            form.repo_btn.setText(ru_RU.get()['repo_btn'])
        except Exception as e:
            pass
    elif language == 'English':
        try:
            mainclass.setWindowTitle(en_US.get()['about_tt'])
            form.description_label.setText(en_US.get()['free_sft'].format(QT_VERSION_STR, PYQT_VERSION_STR))
            form.label.setText(en_US.get()['gpl_info'])
            form.repo_btn.setText(en_US.get()['repo_btn'])
        except Exception as e:
            pass

