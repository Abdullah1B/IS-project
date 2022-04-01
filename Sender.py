import socket
import database as db
from getpass import getpass


HOST = ""
PORT = 5021
FORMAT = "utf-8"
HEADERSIZE = 1024

ADMIN = "admin"
PASS = "admin123"


class Sender(object):

    def __init__(self, HostIP, port):
        self.Host = HostIP
        self.Port = port

    def login(self, username, password) -> bool:
        if db.Get_User(username, password):
            if username == ADMIN:
                print("Login successfully\n Welcome {}".format(username))
            return True
        else:
            print("Username or Password is wrong")
            return False

    def menu(self, username):

        if username == 'admin':
            choice = input("1-Create new User\n2-SendFile\n--> ")

            if int(choice) == 1:
                self.create_user()
            else:
                self.send_File()

        else:
            self.send_File()

    def create_user(self):
        while True:
            Username = input("Enter Username: ")
            Password = input("Enter Password: ")
            if self.check_User(Username, Password):
                if db.Create_User(Username=Username, Password=Password):
                    print(
                        "New user -->\nUsername [{}]\nPassword [{}]".format(Username, Password))
                    break
                else:
                    print("Username is already exists")

    def check_User(self, Username: str, Password: str) -> bool:
        alphbate = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

        if (len(Password) < 6 or len(Password) > 16):
            print("The length of password must be between 6 and 16")
            return False
        if (" " in Username or Username[0].isdigit() or not Username[0] in alphbate):
            print(
                "Useraname must not contin any space\nUsername must start with character..")
            return False
        return True

    def send_File(self):
        print("here send_File ")
        pass

    def handle_client(self, client, address):
        pass

    def Start(self):
        while True:
            Username = input("Username: ")
            Password = getpass("Password:")

            if self.login(Username, Password):
                self.menu(Username)
                break


if __name__ == "__main__":
    s = Sender(HOST, PORT)
    s.Start()
