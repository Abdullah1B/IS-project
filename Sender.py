from ast import dump
import socket
import os
from tqdm import tqdm
from getpass import getpass
from Crypto.Cipher import AES , PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64encode
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad
from Crypto.Random import get_random_bytes


HOST = "127.0.0.1"
PORT = 5555
FORMAT = "utf-8"
HEADERSIZE = 64

# PASSWORD = ""


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
                self.UNAME = Username
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
                self.Sender_Socket.send("Register".encode(FORMAT))
                self.send_data("{}+{}+{}".format(Username,Password,self.pair_key(Username)))
                if self.receive_data() == "OK":
                    print(
                        "New user -->\nUsername [{}]\nPassword [{}]".format(Username, Password))
                    self.handle_client()
                    break
                else:
                    print("Username is already exists")
                    

    def check_User(self, Username: str, Password: str) -> bool:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        if (len(Password) < 6 or len(Password) > 16):
            print("The length of password must be between 6 and 16")
            return False
        if (" " in Username or not Username[0] in alphabet  ):
            print(
                "Useraname must not contin any space\nUsername must start with character..")
            return False
        return True

    def encyrpted_key(self,public_key,session_key):
        with open(public_key,'r') as f:
            key = RSA.import_key( f.read())

        cipher_rsa = PKCS1_OAEP.new(key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        return enc_session_key






    def dencyrpted_key(self,private_key,data): 
    
        with open(private_key,'r') as f:
            key = RSA.import_key( f.read())

        cipher_rsa = PKCS1_OAEP.new(key)
        enc_session_key = cipher_rsa.decrypt(data)

        return enc_session_key


        


    def pair_key(self,username):
        key_pair = RSA.generate(1024)
        public_key = key_pair.publickey().export_key()
        with open('private\\{}.key'.format(username),'wb') as f:
            f.write(key_pair.export_key())
        path = 'keys\\public-{}.key'.format(username)
        with open(path,'wb') as f:
            f.write(public_key)

        return path

    def handle_client(self):

        connection = True
        input_key = self.main_menu() 
        while connection:

            if input_key == '1':

                self.send_data("{}+{}".format(input("Enter friend username: "),self.UNAME))
                URL = input("Enter the Url of File (location): ")
                self.send_file(URL)
                print(self.Sender_Socket.recv(128).decode())

               

                input_key = self.main_menu()

            elif input_key == '2': 
                self.send_data(self.UNAME)

                message = self.receive_data()
                response = input("Do want to open the messages? [Yes Or No]\n-> ").upper()
                
                self.send_data(response)
                if response == 'YES':
                    self.receive_file()


                print(self.receive_data().split('+')[1:])
                input_key = self.main_menu()

            elif input_key == '3':  
                print("")
                self.send_data("Disconnecting....")
                self.receive_data()
                connection = False

            else: 
                print("ENTER NUMBER BETWEEN 1-3 ...... ")
                input_key = self.main_menu()


    def send_file(self,URL):# change Url to ????? don't forget
       
        with open(URL,'rb') as f:
            byte_read = f.read()



        public_receiver = self.Sender_Socket.recv(128)

        sec_key = get_random_bytes(16)

        cipher = AES.new(sec_key,AES.MODE_CBC)

        iv = cipher.iv 

        chiper_text = cipher.encrypt(pad(byte_read,AES.block_size))

        filesize = len(chiper_text)
        newKey = self.encyrpted_key(public_receiver,sec_key)
        newIV = self.encyrpted_key(public_receiver,iv)

        self.Sender_Socket.send(("{}<SBER>{}".format(URL.split('\\')[-1], filesize)).encode(FORMAT))

        # Encrypt it by using public key of receiver
        # self.Sender_Socket.send( newKey )
        # self.Sender_Socket.send( newIV  )
        self.Sender_Socket.send(self.save_key(newKey,newIV).encode(FORMAT))
        

        self.Sender_Socket.send(chiper_text)
    
    def save_key(self,key,iv):
        
        iv = b64encode(iv).decode('utf-8')
        key = b64encode(key).decode('utf-8')
        
        keys = json.dumps({'iv':iv,'key':key})
        path = 'sessionKey\\{}.json'.format(self.UNAME)

        with open(path,'w') as f:
            json.dump(keys , f , indent= 2)
        return path

    def receive_file(self):
        self.Sender_Socket.recv()
        self.Sender_Socket.recv()
        self.Sender_Socket.recv()

        pass





























    def send_data(self,message): # delete it 

        message2 = str(message)
        message2 = f'{len(message2):<{HEADERSIZE}}' + message2 
        self.Sender_Socket.send(message2.encode(FORMAT)) 
    
    
    def receive_data(self):# delete it
      
        full_message = ''
        new_msg = True
        while True:

            msg = self.Sender_Socket.recv(64)  
            if new_msg: 
                msg_length = int(msg[:HEADERSIZE]) 
                new_msg = False
            full_message += msg.decode(FORMAT)

            if len(full_message) - HEADERSIZE == msg_length: 
                print(
                    f"Received message from server: {full_message[HEADERSIZE:]}\n")
                new_msg = True
                message = full_message[HEADERSIZE:]
                full_message = ''
                return message

    def Start(self):
        self.Sender_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.Sender_Socket.connect((HOST,PORT))
        self.menu()
    
if __name__ == "__main__":
    
    s = Sender()
    s.Start()
