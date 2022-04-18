import sys
import PyQt5 as Q5
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import PyQt5.QtGui as GU
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QApplication, QWidget ,QStackedWidget,QMainWindow,QLabel
from PyQt5.QtQuickWidgets import QtQuickWidgets

class gui(QMainWindow):
    def __init__(self): 
        super(gui,self).__init__()



        loadUi("GUI\main_page.ui",self)
        self.hide = True
        self.main_fram =self.findChild(QLabel,"label_100") 
        self.label = self.findChild(QLabel,"label")
        self.username_label = self.findChild(qtw.QLineEdit,"username")
        self.Resgister = self.findChild(qtw.QPushButton,"bt2")
        self.Login = self.findChild(qtw.QPushButton,"bt1")
        self.Login2 = self.findChild(qtw.QPushButton,"bt4")
        self.Sing_up = self.findChild(qtw.QPushButton,"bt3")
        self.password_label = self.findChild(qtw.QLineEdit,"password")
        self.widg = self.findChild(QWidget,"widget_4")
        if self.hide:
            self.widg.hide()

        # self.login_form = self.findChild(QWidget,"widget3")
        shadow = qtw.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(35)
        shadow.setOffset(5)         
        shadow4 = qtw.QGraphicsDropShadowEffect()
        shadow4.setBlurRadius(35)
        shadow4.setOffset(5) 
 

        GU.QFontDatabase.addApplicationFont("Poppins-Regular.ttf")

        

        shadow2 = qtw.QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(35)
        shadow3 = qtw.QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(35)
        # self.login_form.setGraphicsEffect(shadow)
        shadow2.setOffset(5) 
        shadow3.setOffset(5)        
        # self.username_label.setGraphicsEffect(shadow2)
        # self.password_label.setGraphicsEffect(shadow3)
        self.Login.setGraphicsEffect(shadow)
        self.Sing_up.setGraphicsEffect(shadow4)
        self.backgrund = QPixmap("GUI\\cyber-security-2296269_640.jpg")
        # pixmap4 =  self.backgrund.scaled(791, 661, Q5.QtCore.Qt.IgnoreAspectRatio)
        # self.main_fram.setPixmap(pixmap4)

        # shadow.setColor(GU.QColor(14, 62, 218))
        # shadow2.setColor(GU.QColor(14, 62, 218))
        # shadow3.setColor(GU.QColor(14, 62, 218))
        # self.bt = self.findChild(qtw.QPushButton,"bt1")
        # self.bt.clicked.connect(self.clicker)
        self.Resgister.clicked.connect(self.clicker)
        self.Login2.clicked.connect(self.login_form)
        self.i = 0
        self.images = ["GUI\\cat.0.jpg","GUI\\cat.1.jpg","GUI\\cat.2.jpg"]
        # print("hello")
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.changeImg)
        # self.timer.start(5000)
        # # self.changeImg()
    def login_form(self):
        self.widg.hide()
        self.hide = True 
    def clicker(self):
        self.hide = False
        self.widg.show()
    def changeImg(self):
        if self.i < len(self.images):
            self.Pixmap = QPixmap(self.images[self.i])
            self.label.setPixmap(self.Pixmap)
            self.i +=1
        else:
            self.i = 0
            


app = QApplication(sys.argv)

main = gui() 
widget = QStackedWidget()
main.show()
# widget.addWidget(main)
# widget.setWindowFlags(Q5.QtCore.Qt.FramelessWindowHint|Q5.QtCore.Qt.WindowMaximizeButtonHint)
# widget.setFixedHeight(605)
# widget.setFixedWidth(1278)
# widget.show()

try:
    sys.exit(app.exec_())
except:
    print("hrfevd")