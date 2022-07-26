# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main2.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        MainWindow.setMinimumSize(QtCore.QSize(1366, 768))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 5, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 2, 3, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 4, 1, 1)
        self.image_list = QtWidgets.QListWidget(self.centralwidget)
        self.image_list.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.image_list.setFont(font)
        self.image_list.setMouseTracking(True)
        self.image_list.setObjectName("image_list")
        self.gridLayout.addWidget(self.image_list, 4, 3, 1, 1)
        self.tag_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.tag_tab.setMinimumSize(QtCore.QSize(300, 0))
        self.tag_tab.setMaximumSize(QtCore.QSize(400, 16777215))
        self.tag_tab.setObjectName("tag_tab")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dir_list = QtWidgets.QListWidget(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.dir_list.setFont(font)
        self.dir_list.setObjectName("dir_list")
        self.gridLayout_2.addWidget(self.dir_list, 0, 0, 1, 1)
        self.tag_tab.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.anno_list = QtWidgets.QListWidget(self.tab_4)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.anno_list.setFont(font)
        self.anno_list.setMouseTracking(True)
        self.anno_list.setObjectName("anno_list")
        self.gridLayout_4.addWidget(self.anno_list, 0, 0, 1, 1)
        self.tag_tab.addTab(self.tab_4, "")
        self.gridLayout.addWidget(self.tag_tab, 1, 3, 1, 1)
        self.main_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.main_tab.setMinimumSize(QtCore.QSize(1000, 0))
        self.main_tab.setObjectName("main_tab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem6, 4, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem7, 2, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem8, 3, 2, 1, 1)
        self.image_name = QtWidgets.QLabel(self.tab)
        self.image_name.setMinimumSize(QtCore.QSize(0, 25))
        self.image_name.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.image_name.setFont(font)
        self.image_name.setObjectName("image_name")
        self.gridLayout_3.addWidget(self.image_name, 1, 1, 1, 1)
        self.image = QtWidgets.QLabel(self.tab)
        self.image.setMinimumSize(QtCore.QSize(800, 600))
        self.image.setStyleSheet("QLabel{background-color: rgba(127,127,127,0.8);}")
        self.image.setText("")
        self.image.setObjectName("image")
        self.gridLayout_3.addWidget(self.image, 3, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem9, 0, 1, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem10, 3, 0, 1, 1)
        self.main_tab.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.user = QtWidgets.QLineEdit(self.tab_2)
        self.user.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.user.setFont(font)
        self.user.setMaxLength(32)
        self.user.setObjectName("user")
        self.gridLayout_5.addWidget(self.user, 0, 1, 1, 1)
        self.login_out = QtWidgets.QPushButton(self.tab_2)
        self.login_out.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.login_out.setFont(font)
        self.login_out.setObjectName("login_out")
        self.gridLayout_5.addWidget(self.login_out, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)
        self.password = QtWidgets.QLineEdit(self.tab_2)
        self.password.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.password.setFont(font)
        self.password.setMaxLength(32)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridLayout_5.addWidget(self.password, 1, 1, 1, 1)
        self.connection_status = QtWidgets.QLabel(self.tab_2)
        self.connection_status.setStyleSheet("QLabel{background-color: rgb(255,70,70);}")
        self.connection_status.setAlignment(QtCore.Qt.AlignCenter)
        self.connection_status.setObjectName("connection_status")
        self.gridLayout_5.addWidget(self.connection_status, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 2, 0, 1, 1)
        self.ip = QtWidgets.QLineEdit(self.tab_2)
        self.ip.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.ip.setFont(font)
        self.ip.setObjectName("ip")
        self.gridLayout_5.addWidget(self.ip, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 4, 0, 1, 1)
        self.labels_name = QtWidgets.QPlainTextEdit(self.tab_2)
        self.labels_name.setMaximumSize(QtCore.QSize(350, 65535))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labels_name.setFont(font)
        self.labels_name.setObjectName("labels_name")
        self.gridLayout_5.addWidget(self.labels_name, 4, 1, 1, 1)
        self.Tips = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        self.Tips.setFont(font)
        self.Tips.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Tips.setObjectName("Tips")
        self.gridLayout_5.addWidget(self.Tips, 0, 3, 5, 1)
        self.port = QtWidgets.QSpinBox(self.tab_2)
        self.port.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.port.setFont(font)
        self.port.setMinimum(1)
        self.port.setMaximum(65535)
        self.port.setProperty("value", 12345)
        self.port.setObjectName("port")
        self.gridLayout_5.addWidget(self.port, 3, 1, 1, 1)
        self.main_tab.addTab(self.tab_2, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.local_pwd = QtWidgets.QLineEdit(self.tab_5)
        self.local_pwd.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.local_pwd.setFont(font)
        self.local_pwd.setMaxLength(32)
        self.local_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.local_pwd.setObjectName("local_pwd")
        self.gridLayout_6.addWidget(self.local_pwd, 1, 1, 1, 1)
        self.localService = QtWidgets.QCheckBox(self.tab_5)
        self.localService.setObjectName("localService")
        self.gridLayout_6.addWidget(self.localService, 6, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab_5)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_6.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab_5)
        self.label_8.setMinimumSize(QtCore.QSize(90, 0))
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_6.addWidget(self.label_8, 0, 0, 1, 1)
        self.local_user = QtWidgets.QLineEdit(self.tab_5)
        self.local_user.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.local_user.setFont(font)
        self.local_user.setMaxLength(32)
        self.local_user.setObjectName("local_user")
        self.gridLayout_6.addWidget(self.local_user, 0, 1, 1, 1)
        self.rootPath = QtWidgets.QLineEdit(self.tab_5)
        self.rootPath.setMinimumSize(QtCore.QSize(0, 25))
        self.rootPath.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.rootPath.setFont(font)
        self.rootPath.setObjectName("rootPath")
        self.gridLayout_6.addWidget(self.rootPath, 5, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.tab_5)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_6.addWidget(self.label_10, 4, 0, 1, 1)
        self.local_port = QtWidgets.QSpinBox(self.tab_5)
        self.local_port.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.local_port.setFont(font)
        self.local_port.setMinimum(1)
        self.local_port.setMaximum(65535)
        self.local_port.setProperty("value", 12345)
        self.local_port.setObjectName("local_port")
        self.gridLayout_6.addWidget(self.local_port, 4, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem11, 1, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.tab_5)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_6.addWidget(self.label_11, 5, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab_5)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_6.addWidget(self.label_9, 1, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem12, 8, 1, 1, 1)
        self.local_host = QtWidgets.QLineEdit(self.tab_5)
        self.local_host.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.local_host.setFont(font)
        self.local_host.setObjectName("local_host")
        self.gridLayout_6.addWidget(self.local_host, 2, 1, 1, 1)
        self.wrongrootpath = QtWidgets.QLabel(self.tab_5)
        self.wrongrootpath.setStyleSheet("QLabel{color:red;}")
        self.wrongrootpath.setObjectName("wrongrootpath")
        self.gridLayout_6.addWidget(self.wrongrootpath, 7, 1, 1, 1)
        self.main_tab.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.main_tab, 1, 1, 4, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1366, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tag_tab.setCurrentIndex(0)
        self.main_tab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RemoteLabel"))
        self.label_7.setText(_translate("MainWindow", "图片列表"))
        self.tag_tab.setTabText(self.tag_tab.indexOf(self.tab_3), _translate("MainWindow", "图片文件夹列表"))
        self.tag_tab.setTabText(self.tag_tab.indexOf(self.tab_4), _translate("MainWindow", "标签列表"))
        self.image_name.setText(_translate("MainWindow", "image name"))
        self.main_tab.setTabText(self.main_tab.indexOf(self.tab), _translate("MainWindow", "图像"))
        self.label.setText(_translate("MainWindow", "用户名"))
        self.user.setText(_translate("MainWindow", "admin"))
        self.login_out.setText(_translate("MainWindow", "登录"))
        self.label_2.setText(_translate("MainWindow", "密码"))
        self.password.setText(_translate("MainWindow", "admin"))
        self.connection_status.setText(_translate("MainWindow", "disconnect"))
        self.label_3.setText(_translate("MainWindow", "IP地址/域名"))
        self.ip.setText(_translate("MainWindow", "127.0.0.1"))
        self.label_4.setText(_translate("MainWindow", "端口号"))
        self.label_5.setText(_translate("MainWindow", "标签名"))
        self.labels_name.setPlainText(_translate("MainWindow", "dog\n"
"cat\n"
""))
        self.Tips.setText(_translate("MainWindow", "HotKeys\n"
"Ctrl+W   draw/cancel draw new boundingbox\n"
"Ctrl+Q   previous image\n"
"Ctrl+E   next image\n"
"Ctrl+S   save changes\n"
"Delete   delete current label"))
        self.main_tab.setTabText(self.main_tab.indexOf(self.tab_2), _translate("MainWindow", "设定"))
        self.local_pwd.setText(_translate("MainWindow", "admin"))
        self.localService.setText(_translate("MainWindow", "开启本地服务"))
        self.label_6.setText(_translate("MainWindow", "Host"))
        self.label_8.setText(_translate("MainWindow", "登录用户名"))
        self.local_user.setText(_translate("MainWindow", "admin"))
        self.rootPath.setText(_translate("MainWindow", "./images"))
        self.label_10.setText(_translate("MainWindow", "服务端口号"))
        self.label_11.setText(_translate("MainWindow", "数据集根目录"))
        self.label_9.setText(_translate("MainWindow", "登录密码"))
        self.local_host.setText(_translate("MainWindow", "0.0.0.0"))
        self.wrongrootpath.setText(_translate("MainWindow", "该目录不存在！"))
        self.main_tab.setTabText(self.main_tab.indexOf(self.tab_5), _translate("MainWindow", "本地服务"))
