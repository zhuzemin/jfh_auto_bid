# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(799, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 460, 331, 81))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_launchFirefox = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_launchFirefox.setGeometry(QtCore.QRect(10, 30, 91, 23))
        self.pushButton_launchFirefox.setObjectName("pushButton_launchFirefox")
        self.groupBox_iMacros = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_iMacros.setGeometry(QtCore.QRect(120, 10, 191, 51))
        self.groupBox_iMacros.setObjectName("groupBox_iMacros")
        self.pushButton_Start = QtWidgets.QPushButton(self.groupBox_iMacros)
        self.pushButton_Start.setGeometry(QtCore.QRect(10, 20, 51, 23))
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.pushButton_Pause = QtWidgets.QPushButton(self.groupBox_iMacros)
        self.pushButton_Pause.setGeometry(QtCore.QRect(70, 20, 51, 23))
        self.pushButton_Pause.setObjectName("pushButton_Pause")
        self.pushButton_Cancel = QtWidgets.QPushButton(self.groupBox_iMacros)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(130, 20, 51, 23))
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 20, 761, 431))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_addProfile = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_addProfile.setEnabled(True)
        self.pushButton_addProfile.setGeometry(QtCore.QRect(680, 20, 65, 21))
        self.pushButton_addProfile.setObjectName("pushButton_addProfile")
        self.lineEdit_url = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_url.setGeometry(QtCore.QRect(50, 20, 611, 21))
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label.setObjectName("label")
        self.tableView_threadList = QtWidgets.QTableView(self.groupBox_2)
        self.tableView_threadList.setGeometry(QtCore.QRect(10, 50, 741, 371))
        self.tableView_threadList.setObjectName("tableView_threadList")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(370, 460, 161, 81))
        self.groupBox_4.setObjectName("groupBox_4")
        self.checkBox_debugEnable = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_debugEnable.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.checkBox_debugEnable.setObjectName("checkBox_debugEnable")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 91, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_stepInterval = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_stepInterval.setGeometry(QtCore.QRect(110, 50, 31, 20))
        self.lineEdit_stepInterval.setObjectName("lineEdit_stepInterval")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(550, 490, 231, 21))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 799, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Control"))
        self.pushButton_launchFirefox.setText(_translate("MainWindow", "launchFirefox"))
        self.groupBox_iMacros.setTitle(_translate("MainWindow", "iMacros"))
        self.pushButton_Start.setText(_translate("MainWindow", "Start"))
        self.pushButton_Pause.setText(_translate("MainWindow", "Pause"))
        self.pushButton_Cancel.setText(_translate("MainWindow", "Cancel"))
        self.groupBox_2.setTitle(_translate("MainWindow", "threadList"))
        self.pushButton_addProfile.setText(_translate("MainWindow", "Add"))
        self.label.setText(_translate("MainWindow", "Url: "))
        self.groupBox_4.setTitle(_translate("MainWindow", "Debug"))
        self.checkBox_debugEnable.setText(_translate("MainWindow", "debugEnable"))
        self.label_2.setText(_translate("MainWindow", "stepInterval: "))
