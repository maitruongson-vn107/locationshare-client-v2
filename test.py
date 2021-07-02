# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget,QDialog
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QVBoxLayout
import re
import json
from urllib.request import urlopen
import requests
from city import a

import json
print(len(a))
base = "http://127.0.0.1:5000/"

gps_url = 'http://ipinfo.io/json'
response = urlopen(gps_url)
gps_data = json.load(response)
#
# ip = gps_data['ip']
# org = gps_data['org']
# city = gps_data['city']
# country = gps_data['country']
# region = gps_data['region']
# print('Ip: {0}, org: {1}, city: {2}, country: {3}, region: {4}'.format(ip,org,city,country,region))


list = []

class App(QStackedWidget):
    login_size = {
        "width":350,
        "height":200
    }
    main_size = {
        "width":350,
        "height":550
    }
    def resize(self,scene = "login_size"):
        if (scene == "login_size"):
            self.setFixedWidth(App.login_size["width"])
            self.setFixedHeight(App.login_size["height"])
        else:
            self.setFixedWidth(App.main_size["width"])
            self.setFixedHeight(App.main_size["height"])
    def __init__(self):
        super(App,self).__init__()
        login = LoginForm(self)
        main_window = MainWindow(self)
        self.addWidget(login)
        self.setWindowTitle("Location Sharing")
        self.addWidget(main_window)
        self.setFixedWidth(350)
        self.setFixedHeight(200)
        self.resize("login_size")
class LoginForm(QWidget):
    def __init__(self,manager= None):
        super(LoginForm,self).__init__()
        self.manager = manager
        uic.loadUi('login.ui',self)
        self.pushButton.clicked.connect(self.toMain)
        self.pushButton_3.clicked.connect(self.newLoginForm)
    def toMain(self):
        self.manager.setCurrentIndex(self.manager.currentIndex() + 1)
        self.manager.resize("main_size")
        #self.manager.currentWidget().label.setText("")
    def newLoginForm(self):
        new_window = App()
        list.append(new_window)
        new_window.show()

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        #self.manager = manager
        uic.loadUi('test.ui',self)
        self.lay = QVBoxLayout()
        self.scrollAreaWidgetContents.setLayout(self.lay)
        # unit user
        for i in range(5):
            horizontalLayoutWidget = QtWidgets.QWidget()
            horizontalLayoutWidget.setGeometry(QtCore.QRect(220, 20, 160, 54))
            horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
            horizontalLayout = QtWidgets.QHBoxLayout(horizontalLayoutWidget)
            horizontalLayout.setContentsMargins(0, 0, 0, 0)
            horizontalLayout.setObjectName("horizontalLayout")
            self.lay.addWidget(horizontalLayoutWidget)
            # ava
            label = QtWidgets.QLabel(horizontalLayoutWidget)
            label.setText("")
            label.setPixmap(QtGui.QPixmap("ava.png"))
            label.setObjectName("label")
            horizontalLayout.addWidget(label)

            # inforbox
            verticalLayout = QtWidgets.QVBoxLayout()
            verticalLayout.setObjectName("verticalLayout")
            horizontalLayout.addLayout(verticalLayout)

            # name
            label_2 = QtWidgets.QLabel(horizontalLayoutWidget)
            label_2.setObjectName("label_2")
            label_2.setText("Huy")
            verticalLayout.addWidget(label_2)
            # age
            label_3 = QtWidgets.QLabel(horizontalLayoutWidget)
            label_3.setObjectName("label_3")
            label_3.setText("Huy, 21")
            verticalLayout.addWidget(label_3)
        # pushButton_2.clicked.connect(toLogin)
        # self.pushButton.clicked.connect(self.search)
        # for i in range(64):
        #     self.comboBox.addItem("")
        # _translate = QtCore.QCoreApplication.translate
        # for i in range(64):
        #     self.comboBox.setItemText(i, _translate("Form", a[i]["province"]))

        # t = QHBoxLayout()
        # img = QLabel(self)
        # pixmap = QPixmap('ava.png')
        # img.setPixmap(pixmap)
        # t.addWidget(img)
        # self.scrollArea.widget().children().insert(2,t)
        # self.scrollArea.widget().children().insert(3,t)
        # self.scrollArea.widget().children().insert(4,t)
        # self.scrollArea.widget().children().insert(5,t)


        print(self.scrollAreaWidgetContents)
    # def toLogin(self):
    #     self.manager.setCurrentIndex(self.manager.currentIndex() - 1)
    #     self.manager.resize("login_size")
    # def search(self):
    #
    #
    #     for a in self.verticalLayout.children():
    #         a.hide()
    #     # response = requests.get(base + 'h')
    #     users = [1,2,3,4,5]
    #     # create a user box
    #     for user in users:
    #         horizontalLayout_2 = QtWidgets.QHBoxLayout()
    #         list.append(horizontalLayout_2)
    #         horizontalLayout_2.setSpacing(10)
    #         # self.horizontalLayout_2.setObjectName("horizontalLayout_2")
    #         # avatar img
    #         label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
    #         list.append(label_4)
    #         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    #         sizePolicy.setHorizontalStretch(0)
    #         sizePolicy.setVerticalStretch(0)
    #         sizePolicy.setHeightForWidth(label_4.sizePolicy().hasHeightForWidth())
    #         label_4.setSizePolicy(sizePolicy)
    #         label_4.setText("")
    #         label_4.setPixmap(QtGui.QPixmap("ava.png"))
    #         # self.label_4.setObjectName("label_4")
    #         horizontalLayout_2.addWidget(label_4)
    #         # infor box
    #         verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
    #         list.append(verticalLayout_2)
    #         #verticalLayout_2.setObjectName("verticalLayout_2")
    #         # first line infor
    #         label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
    #         list.append(label)
    #         #self.label.setObjectName("label")
    #         verticalLayout_2.addWidget(label)
    #         # second line infor
    #         label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
    #         list.append(label_3)
    #         #label_3.setObjectName("label_3")
    #         verticalLayout_2.addWidget(label_3)
    #
    #         horizontalLayout_2.addLayout(verticalLayout_2)
    #         self.verticalLayout.addLayout(horizontalLayout_2)
app = QApplication(sys.argv)
widgets = MainWindow()
#list.append(widgets)
widgets.show()

try:
    sys.exit(app.exec_())
except:
    print('Closing')