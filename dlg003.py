# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '003.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(368, 302)
        Dialog.setMinimumSize(QtCore.QSize(368, 302))
        Dialog.setStyleSheet("background-color: rgb(43, 43, 43);\n"
"color: rgb(255, 255, 255);")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setStyleSheet("selection-background-color: rgb(255, 119, 0);")
        self.tabWidget.setObjectName("tabWidget")
        self.main_tab = QtWidgets.QWidget()
        self.main_tab.setObjectName("main_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.main_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.authmethod_combo = QtWidgets.QComboBox(self.main_tab)
        self.authmethod_combo.setEnabled(True)
        self.authmethod_combo.setMinimumSize(QtCore.QSize(0, 20))
        self.authmethod_combo.setStyleSheet("selection-background-color: rgb(161, 75, 0);")
        self.authmethod_combo.setObjectName("authmethod_combo")
        self.gridLayout.addWidget(self.authmethod_combo, 4, 1, 1, 1)
        self.profname_label = QtWidgets.QLabel(self.main_tab)
        self.profname_label.setMinimumSize(QtCore.QSize(126, 0))
        self.profname_label.setMaximumSize(QtCore.QSize(126, 16777215))
        self.profname_label.setObjectName("profname_label")
        self.gridLayout.addWidget(self.profname_label, 0, 0, 1, 1)
        self.authm_label = QtWidgets.QLabel(self.main_tab)
        self.authm_label.setMinimumSize(QtCore.QSize(126, 0))
        self.authm_label.setMaximumSize(QtCore.QSize(126, 16777215))
        self.authm_label.setObjectName("authm_label")
        self.gridLayout.addWidget(self.authm_label, 4, 0, 1, 1)
        self.profname_box = QtWidgets.QLineEdit(self.main_tab)
        self.profname_box.setObjectName("profname_box")
        self.gridLayout.addWidget(self.profname_box, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.nicknames_label = QtWidgets.QLabel(self.main_tab)
        self.nicknames_label.setMinimumSize(QtCore.QSize(126, 0))
        self.nicknames_label.setMaximumSize(QtCore.QSize(126, 16777215))
        self.nicknames_label.setObjectName("nicknames_label")
        self.gridLayout_5.addWidget(self.nicknames_label, 0, 0, 1, 1)
        self.nicknames_combo = QtWidgets.QComboBox(self.main_tab)
        self.nicknames_combo.setMinimumSize(QtCore.QSize(0, 20))
        self.nicknames_combo.setStyleSheet("selection-background-color: rgb(161, 75, 0);")
        self.nicknames_combo.setObjectName("nicknames_combo")
        self.gridLayout_5.addWidget(self.nicknames_combo, 0, 1, 1, 1)
        self.clear_nicknames_btn = QtWidgets.QPushButton(self.main_tab)
        self.clear_nicknames_btn.setMinimumSize(QtCore.QSize(0, 22))
        self.clear_nicknames_btn.setObjectName("clear_nicknames_btn")
        self.gridLayout_5.addWidget(self.clear_nicknames_btn, 0, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_5)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.password_label = QtWidgets.QLabel(self.main_tab)
        self.password_label.setMinimumSize(QtCore.QSize(126, 0))
        self.password_label.setMaximumSize(QtCore.QSize(126, 16777215))
        self.password_label.setObjectName("password_label")
        self.gridLayout_4.addWidget(self.password_label, 1, 0, 1, 1)
        self.password_box = QtWidgets.QLineEdit(self.main_tab)
        self.password_box.setEnabled(True)
        self.password_box.setStyleSheet("selection-background-color: rgb(161, 75, 0);\n"
"border-color: rgb(255, 119, 0);")
        self.password_box.setInputMask("")
        self.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_box.setObjectName("password_box")
        self.gridLayout_4.addWidget(self.password_box, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.frame = QtWidgets.QFrame(self.main_tab)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2.addWidget(self.frame)
        self.tabWidget.addTab(self.main_tab, "")
        self.conn_tab = QtWidgets.QWidget()
        self.conn_tab.setObjectName("conn_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.conn_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_2 = QtWidgets.QFrame(self.conn_tab)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.layoutWidget = QtWidgets.QWidget(self.frame_2)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 326, 90))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.server_label = QtWidgets.QLabel(self.layoutWidget)
        self.server_label.setObjectName("server_label")
        self.gridLayout_2.addWidget(self.server_label, 0, 0, 1, 1)
        self.server_box = QtWidgets.QLineEdit(self.layoutWidget)
        self.server_box.setStyleSheet("selection-background-color: rgb(161, 75, 0);\n"
"border-color: rgb(255, 119, 0);")
        self.server_box.setObjectName("server_box")
        self.gridLayout_2.addWidget(self.server_box, 0, 1, 1, 1)
        self.encoding_label = QtWidgets.QLabel(self.layoutWidget)
        self.encoding_label.setObjectName("encoding_label")
        self.gridLayout_2.addWidget(self.encoding_label, 1, 0, 1, 1)
        self.encoding_combo = QtWidgets.QComboBox(self.layoutWidget)
        self.encoding_combo.setMinimumSize(QtCore.QSize(0, 20))
        self.encoding_combo.setStyleSheet("selection-background-color: rgb(161, 75, 0);\n"
"border-color: rgb(255, 119, 0);")
        self.encoding_combo.setObjectName("encoding_combo")
        self.gridLayout_2.addWidget(self.encoding_combo, 1, 1, 1, 1)
        self.port_box = QtWidgets.QSpinBox(self.layoutWidget)
        self.port_box.setMinimumSize(QtCore.QSize(0, 20))
        self.port_box.setStyleSheet("selection-background-color: rgb(161, 75, 0);\n"
"border-color: rgb(255, 119, 0);")
        self.port_box.setMinimum(1)
        self.port_box.setMaximum(99999)
        self.port_box.setObjectName("port_box")
        self.gridLayout_2.addWidget(self.port_box, 0, 3, 1, 1)
        self.port_label = QtWidgets.QLabel(self.layoutWidget)
        self.port_label.setObjectName("port_label")
        self.gridLayout_2.addWidget(self.port_label, 0, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.tabWidget.addTab(self.conn_tab, "")
        self.ident_tab = QtWidgets.QWidget()
        self.ident_tab.setObjectName("ident_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.ident_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.quitmsg_label = QtWidgets.QLabel(self.ident_tab)
        self.quitmsg_label.setObjectName("quitmsg_label")
        self.gridLayout_3.addWidget(self.quitmsg_label, 0, 0, 1, 1)
        self.quiting_msg_box = QtWidgets.QLineEdit(self.ident_tab)
        self.quiting_msg_box.setStyleSheet("selection-background-color: rgb(161, 75, 0);\n"
"border-color: rgb(255, 119, 0);")
        self.quiting_msg_box.setObjectName("quiting_msg_box")
        self.gridLayout_3.addWidget(self.quiting_msg_box, 0, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.frame_3 = QtWidgets.QFrame(self.ident_tab)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4.addWidget(self.frame_3)
        self.tabWidget.addTab(self.ident_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStyleSheet("selection-background-color: rgb(255, 119, 0);")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Свойства профиля"))
        self.title_label.setText(_translate("Dialog", "Свойства профиля \"(без названия)\""))
        self.profname_label.setText(_translate("Dialog", "Имя:"))
        self.authm_label.setText(_translate("Dialog", "Метод аутентиф-ии:"))
        self.nicknames_label.setText(_translate("Dialog", "Никнеймы:"))
        self.clear_nicknames_btn.setText(_translate("Dialog", "Очистить"))
        self.password_label.setText(_translate("Dialog", "Пароль:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main_tab), _translate("Dialog", "Общие"))
        self.server_label.setText(_translate("Dialog", "Сервер:"))
        self.encoding_label.setText(_translate("Dialog", "Кодировка:"))
        self.port_label.setText(_translate("Dialog", "Порт:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.conn_tab), _translate("Dialog", "Подключение"))
        self.quitmsg_label.setText(_translate("Dialog", "Сообщение при выходе:"))
        self.quiting_msg_box.setText(_translate("Dialog", "Tinelix IRC server (codename Flight, 0.0.2 Alpha)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ident_tab), _translate("Dialog", "Идентификация"))