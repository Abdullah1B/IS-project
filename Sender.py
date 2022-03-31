import socket
import database as db

HOST = ""
PORT = 5021
FORMAT = "utf-8"
HEADERSIZE = 1024

ADMIN = "admin"
PASS = "admin123"
class Sender(object):
    
    def __init__(self, HostIP,port, username, password) -> None:
        self.Host = HostIP
        self.Port = port

        if(self.login(username, password)):
            self.menu(username)    
           


    def login(self,username,password) -> bool:
        if db.Get_User(username,password):
            if username == ADMIN and password == PASS:
                print("Login successfully\n Welcome {}".format(username))
            return True
        else:
            print("username or password is wrong")
            return False

    def menu(self,username):
        
        if username == 'admin':
            choice = input("1-Create new User\n2-SendFile\n--> ")

            if int(choice) == 1:
                self.create_user()
            else:
                self.send_File()
            
        else:
            self.send_File()
    
    def create_user(self):
        Username = input("Enter Username: ")
        Password = input("Enter Password: ")

        db.Create_User(Username=Username,Password=Password)
        print("New user -->\nUsername [{}]\nPassword [{}]".format(Username,Password))
        
    
    def send_File(self):
        print("here send_File ")
        pass




    def handle_client(self, client, address):
        Mode = client.recv(512) # receive the option mode from client 
        Mode = Mode.decode() # convert from byte to string 
        
        connection = True
        while connection:
            
            
            if Mode == "Quit_application":
                msg  = self.receive_data(client= client , address= address)
                self.send_data(client= client,address= address,msg= f"DISCONNECTED from {address[0]} ".upper())
                connection = False
            Mode = client.recv(512) # receive the optin mode from client 
            Mode = Mode.decode()
        client.close() # close the connetion between client and server 
if __name__ == "__main__":
    s = Sender(HOST,PORT,input("Username: "),input("Password: "))