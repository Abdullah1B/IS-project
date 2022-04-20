from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64decode, b64encode
from getpass import getpass
import socket
import json
import uuid
import os

HOST = "127.0.0.1"
PORT = 5555
FORMAT = "utf-8"
HEADERSIZE = 64


class Sender(object):

    def login(self, username, password) -> bool:
        self.Sender_Socket.send("LOGIN".encode(FORMAT))

        self.Sender_Socket.send(
            ("{}<sper>{}".format(username, password)).encode(FORMAT))

        if self.Sender_Socket.recv(16).decode() == "OK":

            return True
        else:
            return False

    def main_menu(self):
        choice = input("1-Send File\n2-Check Messages\n3-Quit\n-> ")
        if choice == '1':
            self.Sender_Socket.send("Send_File".encode(FORMAT))
            return '1'
        elif choice == '2':
            self.Sender_Socket.send("Check_Messages".encode(FORMAT))
            return '2'
        else:
            self.Sender_Socket.send("Quit".encode(FORMAT))
            return '3'

    def menu(self,Mode,username,password,email):
        choice = Mode

        if choice == '1':
            
            Username = username
            Password = password
            self.UNAME = Username
            if self.login(Username, Password):
                return "OK"
            else:
                return "Username or password is wrong"

        elif choice == '2':
            response = self.create_user(username,password)
            if response == 'OK':
                return 'OK'
            else:
                return response
            
        else:
            exit(1)

    def create_user(self,username,password):
        
        Username = username
        Password = password
        response ,condation = self.check_User(Username, Password)
        if condation:
            self.Sender_Socket.send("Register".encode(FORMAT))
            self.Sender_Socket.send(("{}<sper>{}<sper>{}".format(
                Username, Password, self.pair_key(Username))).encode(FORMAT))
            if self.Sender_Socket.recv(16).decode() == "OK":
                self.UNAME = Username

                return "OK"
            else:
                return "Username is already exists"
        else:
            return response


    def check_User(self, Username: str, Password: str) :
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        if (len(Password) < 6 or len(Password) > 16):

            return "Password must be between 6 and 16" ,False 

        if (" " in Username or not Username[0] in alphabet):
            return "Username must not contin any space or start with digit",False
        return "",True

    def encyrpted_key(self, public_key, session_key):
        with open(public_key, 'r') as f:
            key = RSA.import_key(f.read())

        cipher_rsa = PKCS1_OAEP.new(key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        return enc_session_key

    def dencyrpted_key(self, private_key, data):

        with open(private_key, 'r') as f:
            key = RSA.import_key(f.read())

        cipher_rsa = PKCS1_OAEP.new(key)
        dec_session_key = cipher_rsa.decrypt(data)

        return dec_session_key

    def pair_key(self, username):
        key_pair = RSA.generate(1024)
        public_key = key_pair.publickey().export_key()
        with open('private\{}.pem'.format(username), 'wb') as f:
            f.write(key_pair.export_key())
        path = 'keys\public-{}.pem'.format(username)
        with open(path, 'wb') as f:
            f.write(public_key)

        return path

    def handle_client(self,Mode,Username,filePath):

        connection = True
        input_key = Mode

        if input_key == '1':
            self.Sender_Socket.send("Send_File".encode(FORMAT))
            if self.vaildate_user(Username):
                self.Sender_Socket.send(("{}<sper>{}".format(Username,self.UNAME)).encode(FORMAT))
                URL = filePath
                response = self.send_file(URL)
                print(self.Sender_Socket.recv(128).decode())
                return response
            else:
                return "Fail"
            # input_key = self.main_menu()

        elif input_key == '2':
            self.Sender_Socket.send(self.UNAME.encode(FORMAT))

            message = self.Sender_Socket.recv(64).decode()
            if int(message) > 0:
                print("You have {} messgae".format(message))

                response = input("Do want to open the messages? [Yes Or No]\n-> ").upper()

                self.Sender_Socket.send(response.encode(FORMAT))
                if response == 'YES':
                    Files = self.Sender_Socket.recv(512).decode()

                    file_name, sender = self.message(Files.split("<sper>")[1:])

                    self.receive_file(file_name, sender)
                else:
                    self.Sender_Socket.send("NO".encode(FORMAT))
                    print("There is no message")

                # input_key = self.main_menu()

        elif input_key == '3':
            print("")
            connection = False

        else:
            print("ENTER NUMBER BETWEEN 1-3 ...... ")
            # input_key = self.main_menu()
    def vaildate_user(self,username):
        self.Sender_Socket.send(username.encode(FORMAT))
        if self.Sender_Socket.recv(64).decode() == "False":
            return False
        else:
            return True

    def message(self, files):

        sender = []
        file_names = []
        # sperate the sender and files  [0] file name and [1] sender for the previous file so if x is even that file name and if it odd sender
        for x in range(len(files)):
            if x % 2 == 1:
                sender.append(files[x])
            else:
                file_names.append(files[x])

        for i in range(len(sender)):
            print(i + 1, '-File:', file_names[i], '\nsent by:', sender[i])

        choice = int(input("choice file:"))
        return file_names[choice - 1], sender[choice - 1]

    def send_file(self, URL):  # change Url to ????? don't forget
        with open(URL, 'rb') as f:
            byte_read = f.read()

        public_receiver = self.Sender_Socket.recv(128).decode()
        # if public_receiver == " ":
        #     return "Fail" 
        sec_key = get_random_bytes(16)
        cipher = AES.new(sec_key, AES.MODE_CBC)
        chiper_text = cipher.encrypt(pad(byte_read, AES.block_size))
        filesize = len(chiper_text)
        newKey = self.encyrpted_key(public_receiver, sec_key)
        newIV = self.encyrpted_key(public_receiver, cipher.iv)

        self.Sender_Socket.send(("{}<SBER>{}".format(
            URL.split('\\')[-1], filesize)).encode(FORMAT))

        self.Sender_Socket.send(self.save_key(newKey, newIV).encode(FORMAT))

        self.Sender_Socket.send(chiper_text)
        return "OK"
    def save_key(self, key, iv):

        iv = b64encode(iv).decode('utf-8')
        key = b64encode(key).decode('utf-8')

        keys = json.dumps({'iv': iv, 'key': key})

        path = 'sessionKey\{}.json'.format(uuid.uuid1())

        with open(path, 'w') as f:
            json.dump(keys, f, indent=2)
        return path

    def receive_file(self, file_name, sender):

        self.Sender_Socket.send(
            ("{}<sper>{}".format(file_name, sender)).encode(FORMAT))

        file_size, sec_key = self.Sender_Socket.recv(
            4096).decode().split('<sper>')
        file_size = int(file_size)

        with open(sec_key) as f:
            sec_key = json.load(f)

        sec_key = json.loads(sec_key)

        iv = self.dencyrpted_key("private\{}.pem".format(
            self.UNAME), b64decode(sec_key['iv']))
        key = self.dencyrpted_key("private\{}.pem".format(
            self.UNAME), b64decode(sec_key['key']))

        cipher = AES.new(key, AES.MODE_CBC, iv)

        data = self.Sender_Socket.recv(file_size)
        try:
            data = unpad(cipher.decrypt(data), AES.block_size)

        except (ValueError, KeyError):
            pass

        File_name = file_name.split('\\')[-1]
        save_path = input("Enter where do want to save the file:\n-> ")
        path = os.path.join(save_path,File_name)
        with open(path, 'wb') as f:
            f.write(data)

        self.Sender_Socket.send("OK".encode(FORMAT))


    def Start(self):
        self.Sender_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Sender_Socket.connect((HOST, PORT))
        # self.menu()


if __name__ == "__main__":

    s = Sender()
    s.Start()
