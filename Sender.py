import socket
from getpass import getpass


HOST = "127.0.0.1"
PORT = 5555
FORMAT = "utf-8"
HEADERSIZE = 64

ADMIN = "admin"
PASS = "admin123"


class Sender(object):

    def login(self, username, password) -> bool:
        self.Sender_Socket.send("LOGIN".encode(FORMAT))
        self.send_data("{}+{}".format(username,password))
        
        if self.receive_data() == "OK":
            
            print("Login successfully\n Welcome {}".format(username))
            return True
        else:
            print("Username or Password is wrong")
            return False




    def send_file(self):
        self.send_data("Hello")



    def main_menu(self):
        choice = input("1-Send File\n2-Check Messages\n3-Quit")
        if choice == '1':
            self.Sender_Socket.send("Send_File".encode(FORMAT))
            return '1'
        elif choice == '2':
            self.Sender_Socket.send("Check_Messages".encode(FORMAT))
            return '2'
        else:
            self.Sender_Socket.send("Quit".encode(FORMAT))
            return '3'


    def menu(self):
        choice = input("1-Login\n2-Register\n3-Quit\n->")

        if choice == '1':
            while True:
                Username = input("Username: ")
                Password = getpass("Password:")

                if self.login(Username, Password):
                    self.handle_client()
                    break

        elif choice == '2':
            self.create_user()
        else:
            exit(1)

    def create_user(self):
        while True:
            Username = input("Enter Username: ")
            Password = input("Enter Password: ")
            if self.check_User(Username, Password):
                self.Sender_Socket.send("Register")
                self.send_data("{}+{}".format(Username,Password))
                if self.receive_data() == "OK":
                    print(
                        "New user -->\nUsername [{}]\nPassword [{}]".format(Username, Password))
                    self.main_menu()
                    break
                else:
                    print("Username is already exists")
                    

    def check_User(self, Username: str, Password: str) -> bool:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        if (len(Password) < 6 or len(Password) > 16):
            print("The length of password must be between 6 and 16")
            return False
        if (" " in Username or Username[0].isdigit() or not Username[0] in alphabet):
            print(
                "Useraname must not contin any space\nUsername must start with character..")
            return False
        return True


    def handle_client(self):

        connection = True
        input_key = self.main_menu() # display of option menu 
        while connection:

            if input_key == '1':# send in Open Mode
                message = input("Enter the Url of File (location): ")
                self.send_data(message)
                self.receive_data()

                input_key = self.main_menu()

            elif input_key == '2': # send in Secure mode

                message = input("Enter the message: ")

                input_key = self.main_menu()

            elif input_key == '3': # Quit form application  
                print("")
                self.send_data("Disconnecting....")
                self.receive_data()
                connection = False

            else: # in case the clinet enter wrong option in menu
                print("ENTER NUMBER BETWEEN 1-3 ...... ")
                input_key = self.main_menu()


    def send_data(self,message):

        message2 = str(message)
        message2 = f'{len(message2):<{HEADERSIZE}}' + message2 # add the HEADERSIZE to the message
        self.Sender_Socket.send(message2.encode(FORMAT)) # send to srever 
    
    
    def receive_data(self):
      
        full_message = ''
        new_msg = True
        while True:

            msg = self.Sender_Socket.recv(64)  # receive message up to 64 bytes
            if new_msg: # if it a new message then 
                msg_length = int(msg[:HEADERSIZE]) # message lenght up to HEADERSIZE
                new_msg = False
            full_message += msg.decode(FORMAT)# convet the received part of the message from byte to string

            if len(full_message) - HEADERSIZE == msg_length: # if the length of Full message - HEADERSIZE == message length then we received the whole message 
                print(
                    f"Received message from server: {full_message[HEADERSIZE:]}\n")
                new_msg = True
                message = full_message[HEADERSIZE:]
                full_message = ''
                return message

    def Start(self):
        self.Sender_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket and defind the family and type of socket 
        self.Sender_Socket.connect((HOST,PORT))
        self.menu()


if __name__ == "__main__":
    s = Sender()
    s.Start()