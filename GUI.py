import sys
import re
import os
from Sender import Sender
import PyQt5 as Q5
from PyQt5.uic import loadUi
import PyQt5.QtGui as GU
import PyQt5.QtWidgets as qtw
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QFileDialog, QFileIconProvider


class gui(QMainWindow):
    def __init__(self):
        super(gui, self).__init__()
        loadUi("GUI\main_page.ui", self)
        # widget
        self.Sign_up_form = self.findChild(QWidget, "sign_up")
        self.Sign_up_form.hide()
        self.login_form = self.findChild(QWidget, "widget_2")
        # Buttons
        self.login_page_bt = self.findChild(qtw.QPushButton, "bt4")
        self.sign_up_bt = self.findChild(qtw.QPushButton, "bt3")
        self.login_bt = self.findChild(qtw.QPushButton, "bt1")
        self.register_bt = self.findChild(qtw.QPushButton, "bt2")
        # Label
        self.login_image = self.findChild(QLabel, "login_img")
        self.register_image = self.findChild(QLabel, "register_img")
        self.error = self.findChild(QLabel, "error")
        self.error_Re = self.findChild(QLabel, "error_2")
        # Line edit for login
        self.username = self.findChild(qtw.QLineEdit, "username")
        self.password = self.findChild(qtw.QLineEdit, "password")
        # Line edit for sign up
        self.Nusername = self.findChild(qtw.QLineEdit, "username_re")
        self.Npassword = self.findChild(qtw.QLineEdit, "password_3")
        self.Email = self.findChild(qtw.QLineEdit, "email")

        login_img = GU.QMovie("assets\Login.gif")
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
        register_img = GU.QMovie("assets\Sign up.gif")
        self.register_image.setMovie(register_img)
        register_img.start()

    def show_login(self):
        self.Sign_up_form.hide()
        self.register_image.hide()
        login_img = GU.QMovie("assets\Login.gif")
        self.login_image.setMovie(login_img)
        login_img.start()

    def LOGIN(self):

        Username = self.username.text()
        Password = self.password.text()

        if len(Username) == 0 or len(Password) == 0:
            self.error.setText("please write username and password")
        else:
            rsponse = s.menu('1', Username, Password, "")
            if rsponse != "OK":
                self.error.setText(rsponse)
            else:
                main_Page = main_page()
                widget.addWidget(main_Page)
                widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_UP(self):
        Username = self.Nusername.text()
        Password = self.Npassword.text()
        Email = self.Email.text()
        self.error_Re.setText("")

        if len(Username) == 0 or len(Password) == 0 or len(Email) == 0:
            self.error_Re.setText("Please Enter the required field")
        else:

            if self.check_email(Email).lower() == 'vaild':
                self.error_Re.setText("")
                response = s.menu("2", Username, Password, Email)
                if response != 'OK':
                    self.error_Re.setText(response)
                else:
                    main_Page = main_page()
                    widget.addWidget(main_Page)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.error_Re.setText("Invaild Email (ex@test.com)")

    def check_email(self, email: str):
        pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(pattern, email.lower()):
            return 'vaild'
        else:
            return 'Invaild'


class main_page(QMainWindow):
    def __init__(self):
        super(main_page, self).__init__()
        loadUi("GUI\main_page2.ui", self)

        self.attachment_frame = self.findChild(qtw.QFrame, "attachment_frame")
        self.sendFile_frame = self.findChild(qtw.QFrame, "frame_2")
        self.confirm_frame = self.findChild(qtw.QFrame, "frame_3")
        self.messages_frame = self.findChild(qtw.QFrame, "frame_4")
        self.table = self.findChild(qtw.QTableWidget, "tableWidget")

        self.confirm_frame.hide()
        self.attachment_frame.hide()
        self.messages_frame.hide()
        # Labels
        self.attachment_icon = self.findChild(QLabel, "Icon")
        self.file_name_label = self.findChild(QLabel, "file_name")
        self.file_size_label = self.findChild(QLabel, "size")
        self.confirm_label = self.findChild(QLabel, "confirm")
        self.warning = self.findChild(QLabel, "label_2")
        self.warning2 = self.findChild(QLabel, "label_7")
        # Buttons
        self.Send = self.findChild(qtw.QPushButton, "send_bt")
        self.check = self.findChild(qtw.QPushButton, "check")
        self.logout = self.findChild(qtw.QPushButton, "LOGOUT")
        self.Browse = self.findChild(qtw.QPushButton, "Browse")
        self.cancel = self.findChild(qtw.QPushButton, "cancel")
        self.open = self.findChild(qtw.QPushButton, "open")
        self.Send_file = self.findChild(qtw.QPushButton, "send_bt_2")
        self.OK = self.findChild(qtw.QPushButton, "OK")
        self.To = self.findChild(qtw.QLineEdit, "To")

        # Shadows
        self.Send.setGraphicsEffect(self.shadow())
        self.check.setGraphicsEffect(self.shadow())
        self.logout.setGraphicsEffect(self.shadow())
        self.sendFile_frame.setGraphicsEffect(self.shadow())
        self.To.setGraphicsEffect(self.shadow())
        self.attachment_frame.setGraphicsEffect(self.shadow())
        self.Send_file.setGraphicsEffect(self.shadow())
        self.Browse.setGraphicsEffect(self.shadow())
        self.confirm_frame.setGraphicsEffect(self.shadow())
        self.OK.setGraphicsEffect(self.shadow())

        self.Browse.clicked.connect(self.Upload)
        self.cancel.clicked.connect(self.Cancel)
        self.Send.clicked.connect(self.Send_page)
        self.Send_file.clicked.connect(self.SendFile)
        self.OK.clicked.connect(self.Confirm)
        self.logout.clicked.connect(self.Logout)
        self.open.clicked.connect(self.Open)
        self.check.clicked.connect(self.loadData)
        self.table.setColumnWidth(0, 170)
        self.table.setColumnWidth(1, 170)
        self.table.setColumnWidth(2, 50)
        self.table.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

    def Logout(self):
        quit(1)

    def Send_page(self):
        self.messages_frame.hide()

    def Open(self):

        self.warning2.setText("")
        index = self.table.selectedIndexes()
        if len(index) != 0:
            Item_name = self.table.item(index[0].row(), 0)
            Item_sender = self.table.item(index[0].row(), 1)
            file_name = Item_name.text().split('.')[0]
            extension = Item_name.text().split('.')[-1]
            filename = QFileDialog.getSaveFileName(
                self, "Save file", file_name, '(*).{}'.format(extension))
            path_to_save = filename[0]

            if len(path_to_save) > 0:
                response = s.handle_client("2", Username="", filePath=str(
                    path_to_save+'.'+extension), Filename=Item_name.text(), Sender=Item_sender.text())
                if response == "OK":
                    self.table.removeRow(index[0].row())
                    self.attachment_frame.hide()
                    self.file_name_label.setText("")
                    self.confirm_frame.setStyleSheet(
                        "background-color: rgb(255, 255, 255);border-radius: 35px;")
                    self.confirm_frame.show()
                    moive = GU.QMovie("assets\output_LfDsSc.gif")
                    self.confirm_label.setMovie(moive)
                    moive.start()
        else:
            self.warning2.setText("Please select a file...")

    def loadData(self):
        self.messages_frame.show()
        senders, file_names, dates, _ = s.handle_client('3', '', '')
        if senders == "No messages":
            self.table.setItem(row, 0, qtw.QTableWidgetItem("No messages"))

        else:
            row = 0
            self.table.setRowCount(len(file_names))
            for file in file_names:
                self.table.setItem(
                    row, 0, qtw.QTableWidgetItem(file.split('\\')[-1]))
                self.table.setItem(row, 1, qtw.QTableWidgetItem(senders[row]))
                self.table.setItem(row, 2, qtw.QTableWidgetItem(dates[row]))
                row = row+1

    def Confirm(self):
        self.confirm_frame.hide()

    def SendFile(self):
        self.warning.setText("")
        if len(self.To.text()) == 0 or len(self.file_name_label.text()) == 0:
            if len(self.To.text()) == 0:
                self.warning.setText("Please Enter Username")
        else:
            response = s.handle_client("1", self.To.text(), self.fname)
            if response == "OK":
                self.attachment_frame.hide()
                self.file_name_label.setText("")
                self.confirm_frame.setStyleSheet(
                    "background-color: rgb(255, 255, 255);border-radius: 35px;")
                self.confirm_frame.show()
                moive = GU.QMovie("assets\output_LfDsSc.gif")
                self.confirm_label.setMovie(moive)
                moive.start()
            elif response == "not exists":
                self.warning.setText("Username not exists")

    def Cancel(self):
        self.attachment_frame.hide()

    def Upload(self):

        self.fname, _ = QFileDialog.getOpenFileName(
            self, "Open", "", "All Files (*)")

        if len(self.fname) > 0:
            size = os.path.getsize(self.fname)
            icon2 = QFileIconProvider().icon(Q5.QtCore.QFileInfo(self.fname))
            icon = GU.QIcon(icon2)
            icon3 = icon.pixmap(Q5.QtCore.QSize(22, 22), GU.QIcon.Disabled)
            self.attachment_frame.show()
            self.attachment_icon.setPixmap(icon3)
            self.file_size_label.setText(convert_size(size))
            self.file_name_label.setText(self.fname.split('/')[-1])

    def shadow(self):
        shadow3 = qtw.QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(35)
        shadow3.setOffset(5)
        return shadow3


def convert_size(size_bytes):

    if size_bytes >= pow(10, 9):  # GB
        s = round(size_bytes / pow(1024, 3), 2)
        return str(s)+" GB"
    elif size_bytes >= pow(10, 6):  # MB
        s = round(size_bytes / pow(1024, 2), 2)
        return str(s)+" MB"
    elif size_bytes >= 1000:  # KB
        s = round(size_bytes / pow(1024, 1), 2)
        return str(s)+" KB"
    else:  # less than 1kb
        s = round(size_bytes, 2)
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
    pass
