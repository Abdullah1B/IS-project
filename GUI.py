import sys, re, os, math
from Sender import Sender
import PyQt5 as Q5
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import PyQt5.QtGui as GU
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QApplication, QWidget ,QMainWindow,QLabel,QFileDialog,QFileIconProvider

ko = True

class gui(QMainWindow):
    def __init__(self): 
        super(gui,self).__init__()
        loadUi("GUI\main_page.ui",self)
        # widget
        self.Sign_up_form = self.findChild(QWidget,"sign_up")
        self.Sign_up_form.hide()
        self.login_form   = self.findChild(QWidget,"widget_2")
        # Buttons
        self.login_page_bt = self.findChild(qtw.QPushButton,"bt4")
        self.sign_up_bt    = self.findChild(qtw.QPushButton,"bt3")
        self.login_bt      = self.findChild(qtw.QPushButton,"bt1")
        self.register_bt   = self.findChild(qtw.QPushButton,"bt2")
        # Label
        self.login_image    = self.findChild(QLabel,"login_img")  
        self.register_image = self.findChild(QLabel,"register_img")
        self.error = self.findChild(QLabel,"error")
        self.error_Re = self.findChild(QLabel,"error_2")
        # Line edit for login
        self.username = self.findChild(qtw.QLineEdit,"username")
        self.password = self.findChild(qtw.QLineEdit,"password")
        # Line edit for sign up 
        self.Nusername = self.findChild(qtw.QLineEdit,"username_re")
        self.Npassword = self.findChild(qtw.QLineEdit,"password_3")
        self.Email     = self.findChild(qtw.QLineEdit,"email")



        login_img = GU.QMovie("Login.gif")
        self.login_image.setMovie(login_img)
        login_img.start()
        
        self.sign_up_bt.clicked.connect(self.sign_UP)
        self.login_bt.clicked.connect(self.LOGIN) 

        self.register_bt.clicked.connect(self.show_sign)
        self.login_page_bt.clicked.connect(self.show_login)

        # shadow button
        shadow = qtw.QGraphicsDropShadowEffect()                
        shadow.setBlurRadius(35)
        shadow.setOffset(5)        
        shadow2 = qtw.QGraphicsDropShadowEffect()                
        shadow2.setBlurRadius(35)
        shadow2.setOffset(5)   
 
        self.sign_up_bt.setGraphicsEffect(shadow) 
        self.login_bt.setGraphicsEffect(shadow2)
    
    def show_sign(self):
        self.Sign_up_form.show()
        self.register_image.show()
        register_img = GU.QMovie("Sign up (1).gif")
        self.register_image.setMovie(register_img)
        register_img.start()

    def show_login(self):
        self.Sign_up_form.hide()
        self.register_image.hide()
        login_img = GU.QMovie("Login.gif")
        self.login_image.setMovie(login_img)
        login_img.start()

    
    def LOGIN(self):
        Username = self.username.text()
        Password = self.password.text()
        if len(Username) == 0 or len(Password) == 0:
            self.error.setText("please write username and password")
        else:
            rsponse = s.menu('1',Username,Password,"")
            if rsponse != "OK":
                self.error.setText(rsponse)
            else:
                main_Page = main_page()
                widget.addWidget(main_Page)
                widget.setCurrentIndex(widget.currentIndex()+1)
            
    def sign_UP(self):
        Username = self.Nusername.text()
        Password = self.Npassword.text()
        Email    = self.Email.text()
        self.error_Re.setText("")

        if len(Username) == 0 or len(Password) == 0 or len(Email) == 0:
            self.error_Re.setText("Please Enter the required field")
        else:

            if self.check_email(Email).lower() =='vaild':
                self.error_Re.setText("")
                response = s.menu("2",Username,Password,Email)
                if response != 'OK':
                    print(response)
                    self.error_Re.setText(response)
                else:
                    main_Page = main_page()
                    widget.addWidget(main_Page)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.error_Re.setText("Invaild Email (ex@test.com)")
                   

    def check_email(self,email:str):
        pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'  
        if re.search(pattern,email.lower()):
            return 'vaild'
        else:
            return 'Invaild'   

class main_page(QMainWindow):
    def __init__(self): 
        super(main_page,self).__init__()
        loadUi("GUI\main_page2.ui",self)
        self.attachment_frame = self.findChild(qtw.QFrame,"attachment_frame")
        self.sendFile_frame = self.findChild(qtw.QFrame,"frame_2")
        self.attachment_frame.hide()
        self.attachment_icon = self.findChild(QLabel,"Icon")
        self.file_name_label = self.findChild(QLabel,"file_name")
        self.file_size_label = self.findChild(QLabel,"size")
        # Buttons
        self.Send   = self.findChild(qtw.QPushButton,"send_bt")
        self.check  = self.findChild(qtw.QPushButton,"check")
        self.logout = self.findChild(qtw.QPushButton,"LOGOUT")
        self.Browse = self.findChild(qtw.QPushButton,"Browse")
        self.cancel = self.findChild(qtw.QPushButton,"cancel")
        self.Send_file = self.findChild(qtw.QPushButton,"send_bt_2")

        self.To = self.findChild(qtw.QLineEdit,"To")
 
        self.Send.setGraphicsEffect(self.shadow())
        self.check.setGraphicsEffect(self.shadow())
        self.logout.setGraphicsEffect(self.shadow())
        self.sendFile_frame.setGraphicsEffect(self.shadow())
        self.To.setGraphicsEffect(self.shadow())
        self.Browse.clicked.connect(self.pressed)
        self.cancel.clicked.connect(self.Cancel)
        self.Send_file.clicked.connect(self.SendFile)

    def SendFile(self):
        if len(self.To.text()) == 0:
            pass
        else:
            response = s.handle_client("1",self.To.text(),self.fname)
            print(response)

    def Cancel(self):
        self.attachment_frame.hide()
    def pressed(self):

        self.fname, _ = QFileDialog.getOpenFileName(self,"Open", "","All Files (*)")
        
        self.fname = self.fname.replace("/","\\")
        if len(self.fname) >0:
            size = os.path.getsize(self.fname)
            icon2 = QFileIconProvider().icon(Q5.QtCore.QFileInfo(self.fname))
            icon = GU.QIcon(icon2)
            icon3 = icon.pixmap(Q5.QtCore.QSize(22,22),GU.QIcon.Disabled)
            self.attachment_frame.show()
            self.attachment_icon.setPixmap(icon3)
            self.file_size_label.setText(convert_size(size))
            self.file_name_label.setText(self.fname.split('\\')[-1])


    def shadow(self):
        shadow3 = qtw.QGraphicsDropShadowEffect()                
        shadow3.setBlurRadius(35)
        shadow3.setOffset(5)
        return shadow3
def convert_size(size_bytes):

    if size_bytes >= pow(10,9): #GB
        s = round(size_bytes / pow(1024,3),2)
        return str(s)+" GB"
    elif size_bytes >= pow(10,6):#MB
        s = round(size_bytes / pow(1024,2),2)
        return str(s)+" MB"
    elif size_bytes >= 1000:# KB
        s = round(size_bytes / pow(1024,1),2)
        return str(s)+" KB"
    else: # less than 1kb
        s = round(size_bytes,2) 
        return str(s)+" B"



app = QApplication(sys.argv)

main = gui() 

# main.show()
widget = qtw.QStackedWidget()
s = Sender()
s.Start()
widget.addWidget(main)
widget.setFixedHeight(600)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("OFF oOoOoOoOoOoOoOoOoOoOoOoO")