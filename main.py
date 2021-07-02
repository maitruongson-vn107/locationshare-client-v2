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
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QImage,QPixmap
import re
import json
from urllib.request import urlopen
import requests

import threading
import json
from Crypto.Hash import SHA256
base = "http://127.0.0.1:5000/"

# def locate_me():
    
#     country = gps_data['country']
#     region = gps_data['region']
#     print('Ip: {0}, org: {1}, city: {2}, country: {3}, region: {4}'.format(ip,org,city,country,region))
from city import a
i = 0

for d in a:
    d['province_code'] = i
    i += 1

timer = None
list = []
def city_to_code(province:str):
    province_code = '3' #Hà Nội - mặc định
    for x in a:
        if (x['province'] == province):
            province_code = x['province_code']
    return str(province_code)
def code_to_city(code:str):
    province = "Hà Nội" #mặc định
    for x in a:
        if (x['province_code'] == int(code)):
            province = x['province']
    return province

def map_city_vnese(input_str):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
	
    print(input_str.encode('utf-8'))
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s.lower().replace(' ','')
    

map_low_up = {}
class App(QStackedWidget):
    login_size = {
        "width":350,
        "height":200
    }
    main_size = {
        "width":350,
        "height":550
    }
    signup_size = {
        "width": 450,
        "height": 250
    }
    def __init__(self):
        super(App,self).__init__()
        self.login = LoginForm(self)
        self.main_window = MainWindow(self)
        self.addWidget(self.login)
        self.setWindowTitle("Location Sharing")
        self.addWidget(self.main_window)
        self.signup = SignUpForm(self)
        self.addWidget(self.signup)
        self.user  = {"userId":None}
        self.resize("login_size")
        #self.set_interval(self.update_locate_periodicly, 15)


    def resize(self,scene = "login_size"):
        if (scene == "login_size"):
            self.setFixedWidth(App.login_size["width"])
            self.setFixedHeight(App.login_size["height"])
        elif (scene == "main_size"):
            self.setFixedWidth(App.main_size["width"])
            self.setFixedHeight(App.main_size["height"])
        else:
            self.setFixedWidth(App.signup_size["width"])
            self.setFixedHeight(App.signup_size["height"])
    #clear neighbor list
    def clear_data(self):
        self.main_window.clear_data()
        self.login.clear_data()
        self.signup.clear_data()
class SignUpForm(QWidget):
    def __init__(self,manager= None):
        super(SignUpForm,self).__init__()
        self.manager = manager
        uic.loadUi('SignUp.ui',self)
        self.pushButton.clicked.connect(self.signUp)
        self.pushButton_3.clicked.connect(self.toLogin)
    def signUp(self):
        #call sign up api
        gender = 0 if self.comboBox.currentText() == "Male" else 1 if self.comboBox.currentText() == "FeMale" else 2
        sha = SHA256.new(bytes(self.lineEdit_2.text(),'utf-8'))
        hashed_pass = str(sha.hexdigest())
        data = {"username":self.lineEdit.text(),"fullName":self.lineEdit_3.text(), "birthYear":int(self.lineEdit_5.text()),"gender": gender,"password":hashed_pass,
                      "avatarUrl":"ava.png","currentCity":"3"}
        res = requests.post(base+'signUp', json=data).json()
        if (res['msg'] == "success"):
            msg = QMessageBox()
            msg.setWindowTitle("Sign Up Successfully")
            msg.setText("Now you can get started")
            msg.exec_()
            self.toLogin()
            # self.manager.currentWidget().label.setText("")
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Sign Fail")
            msg.setText("Username existed. Please choose another.")
            msg.exec_()
    def toLogin(self):
        self.manager.setCurrentIndex(self.manager.currentIndex() - 2)
        self.manager.clear_data()
        self.manager.resize("login_size")
    def clear_data(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_5.setText("")
class LoginForm(QWidget):
    def __init__(self,manager= None):
        super(LoginForm,self).__init__()
        self.manager = manager
        uic.loadUi('login.ui',self)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_3.clicked.connect(self.newLoginForm)
        self.pushButton_2.clicked.connect(self.toSignUp)
    def toMain(self,user):
        self.manager.setCurrentIndex(self.manager.currentIndex() + 1)
        self.manager.main_window.gen_personal_data(user)
        self.manager.resize("main_size")
        #auto update per 20s   
        # global timer 
        # timer = self.manager.main_window.set_interval(self.manager.main_window.locate_me,5)
    def login(self):
        #call login api
        sha = SHA256.new(bytes(self.lineEdit_2.text(),'utf-8'))
        hashed_pass = str(sha.hexdigest())
        print(hashed_pass)
        data = {'username': self.lineEdit.text(), 'password': hashed_pass}
        res = requests.post(base+'login', json=data).json()
        print(res)
        if (res['msg'] == "success"):
            self.manager.user = res['data']
            self.toMain(self.manager.user)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Login Fail")
            msg.setText("Wrong user name or password")
            msg.exec_()
        return
    def toSignUp(self):
        self.manager.setCurrentIndex(self.manager.currentIndex() + 2)
        self.manager.resize("signup_size")
    def newLoginForm(self):
        new_window = App()
        list.append(new_window)
        new_window.show()
    def clear_data(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
class MainWindow(QWidget):
    def __init__(self,manager= None):
        super(MainWindow,self).__init__()
        self.manager = manager
        uic.loadUi('mainwindow.ui',self)
        self.pushButton_2.clicked.connect(self.toLogin)
        self.pushButton.clicked.connect(self.search)
        self.pushButton_3.clicked.connect(self.locate_me)
        self.pushButton_4.clicked.connect(self.upload_file)
        self.comboBox.view().pressed.connect(self.on_choose)
        #province select dropdown
        for i in range(64):
            self.comboBox.addItem("")
        _translate = QtCore.QCoreApplication.translate
        for i in range(64):
            self.comboBox.setItemText(i, _translate("Form", a[i]["province"]))
            map_low_up[a[i]["province"]] =  map_city_vnese(a[i]["province"])
        self.lay = QVBoxLayout()
        self.scrollAreaWidgetContents.setLayout(self.lay)
        self.lay.setSpacing(10)
        
    
    # def set_interval(self,func, sec):
    #     def func_wrapper():
    #         self.set_interval(func, sec)
    #         func()
    
    #     t = threading.Timer(sec, func_wrapper)
    #     t.start()
    #     return t
    def upload_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")
        imagePath = fname[0]
        if (imagePath != "" and imagePath != None):
            print(self.manager.user['userId'])
            files = {'file': open(imagePath,'rb')}
            userid = self.manager.user['userId']
            values = {'userId':userid}
            res = requests.post(base + 'upload/'+str(userid) , files=files, data=values).json()

            if (res['msg'] != "success"):
                msg = QMessageBox()
                msg.setWindowTitle("Update Fail")
                msg.setText("Server error. Can't change avatar")
                msg.exec_()
            else:
                print(res['data'])
                self.manager.user['avatarUrl'] = res['data']
                self.gen_personal_data(self.manager.user)
        
    def locate_me(self):
        print('auto_locate')
        gps_url = 'http://ipinfo.io/json'
        response = urlopen(gps_url)
        gps_data = json.load(response)  
        
        # ip = gps_data['ip']
        # org = gps_data['org']
        province = gps_data['region']
        print(province)
        province = province.lower().replace(' ','')
        for i in range(64):
            print('so sanh')
            print(map_low_up[self.comboBox.itemText(i)])
            if (province == map_low_up[self.comboBox.itemText(i)]):
                print('find')
                print(i)
                self.comboBox.setCurrentIndex(i)
        # index = self.comboBox.findText(province, QtCore.Qt.MatchFixedString)
        # if index >= 0:
        #     self.comboBox.setCurrentIndex(index)
        location = self.comboBox.currentText()
        print(location)
        city_code = city_to_code(location)
        city_hashed_code = hash_city(city_code)
        data = {'userId': self.manager.user['userId'], 'currentCity': city_hashed_code}
        print('update locate when login')
        print(data)
        res = requests.post(base+'update_locate', json=data).json()
    def on_choose(self,index):
        location = self.comboBox.model().itemFromIndex(index).text()

        city_code = city_to_code(location)
        city_hashed_code = hash_city(city_code)
        data = {'userId': self.manager.user['userId'], 'currentCity': city_hashed_code}
        res = requests.post(base+'update_locate', json=data).json()
        if (res['msg'] != "success"):
            msg = QMessageBox()
            msg.setWindowTitle("Update Fail")
            msg.setText("Server error. Can't change location")
            msg.exec_()

        #call api with location

    def gen_personal_data(self,user):
        #calculate age from date of birth
        # ...
        self.locate_me()
        
        self.label.setText(user['fullName'])
        gender = "Male" if user['gender'] == 0 else "Female" if user['gender'] == 1 else "Third gender"
        self.label_3.setText(gender)
        self.label_6.setText(str(user['age']))
        self.label_4.setText(user['username'])

        url = base + "static/" + user['avatarUrl']
        img = QImage()
        img.loadFromData(requests.get(url).content)
        pim = QPixmap(img)
        pim = pim.scaled(50,50)
        self.label_5.setPixmap(pim)

    def clear_data(self):
        for i in reversed(range(self.lay.count())):
            self.lay.itemAt(i).widget().setParent(None)
    def toLogin(self):
        if (self.manager.user['userId'] != None):
            data = {'userId':self.manager.user['userId']}
            requests.post(base+'logout', json=data).json()
        self.manager.setCurrentIndex(self.manager.currentIndex() - 1)
        self.manager.resize("login_size")
        self.manager.clear_data()
        # timer.cancel()
    def search(self):
        self.clear_data()
        location = self.comboBox.currentText()
        city_code = city_to_code(location)
        city_hashed_code = hash_city(city_code)
        data = {'userId': int(self.manager.user['userId']), 'currentCity': city_hashed_code}
        res = requests.get(base+'search', json=data).json()
        print('Search_result:')
        print(res)
        # users = res
        # users = [{"fullName": "Huy Dang", "age": "21", "gender": "Male"},
        #          {"fullName": "Son Mai", "age": "21", "gender": "Male"}
        #          ]
        # create a user box
        if (False):
            return
        else:
            for u in res['data']:
                horizontalLayoutWidget = QtWidgets.QWidget()
                # horizontalLayoutWidget.setGeometry(QtCore.QRect(220, 20, 160, 54))
                horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
                horizontalLayout = QtWidgets.QHBoxLayout(horizontalLayoutWidget)
                horizontalLayout.setContentsMargins(0, 0, 0, 0)
                horizontalLayout.setObjectName("horizontalLayout")
                horizontalLayoutWidget.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed));
                self.lay.addWidget(horizontalLayoutWidget)
                # ava
                label = QtWidgets.QLabel(horizontalLayoutWidget)
                label.setText("")

                url = base + "static/" + u['avatarUrl']
                img = QImage()
                img.loadFromData(requests.get(url).content)
                pim = QPixmap(img)
                pim = pim.scaled(50,50)
                label.setPixmap(pim)

                
                label.setObjectName("label")
                horizontalLayout.addWidget(label)

                # inforbox
                verticalLayout = QtWidgets.QVBoxLayout()
                verticalLayout.setObjectName("verticalLayout")
                horizontalLayout.addLayout(verticalLayout)

                # name
                label_2 = QtWidgets.QLabel(horizontalLayoutWidget)
                label_2.setObjectName("label_2")
                label_2.setText(u['fullName'])
                verticalLayout.addWidget(label_2)
                # age
                label_3 = QtWidgets.QLabel(horizontalLayoutWidget)
                label_3.setObjectName("label_3")
                gender = 'Male, ' if u['gender'] == 0 else 'Female, ' if u['gender'] == 1 else ''
                label_3.setText(gender + str(u["age"]))
                verticalLayout.addWidget(label_3)

app = QApplication(sys.argv)
widgets = App()
list.append(widgets)
widgets.show()


    
def hash_city(code:str):
    print('hash_code city')
    print(code)
    sha = SHA256.new(bytes(code,'utf-8'))
    hashed_ = int.from_bytes(sha.digest(),'big')
    print('result')
    print(hashed_)
    return str(hashed_)

try:
    sys.exit(app.exec_())
except:
    if (widgets.user['userId'] != None):
        data = {"userId":widgets.user['userId']}
        requests.post(base+'logout', json=data).json()
    print('Closing')
