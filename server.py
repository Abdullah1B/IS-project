import socket
import threading
import database as db
import os
from datetime import datetime


FORMAT = "utf-8"
HEADERSIZE = 64



class server(object):
    def __init__(self, HostIP, port):
        self.HostIP = HostIP
        self.port = port

    def handle_client(self, client, address):

        Mode = client.recv(512)  # receive the option mode from client
        Mode = Mode.decode(FORMAT)  # convert from byte to string

        connection = True
        while connection:
            if Mode == "Send_File":
                query = "SELECT Username from USERS WHERE Username = ('{}')".format(client.recv(128).decode())

                vaildate = db.get(query)
                if vaildate != "False":
                    client.send("True".encode(FORMAT))
                    Username, sender = client.recv(128).decode().split('<sper>')
                    path, session_key = self.receive_file(client, receiver=Username)
                    now = datetime.now()
                    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
                    message = db.add("INSERT INTO Files(name,path,Sender,session_key,date) VALUES('{}','{}','{}','{}','{}')".format(Username, path, sender, session_key,dt_string))
                    if message:
                        client.send("The file sent successfully".encode(FORMAT))
                    else:
                        client.send("Failed".encode(FORMAT))
                else:
                    client.send("False".encode(FORMAT))



            elif Mode == "Check_Messages":
                file_name, Sender, username = client.recv(128).decode().split('<sper>')

                self.send_file(client, file_name, Sender, username)

                # Username = client.recv(128).decode()


                # Files, conut = db.get_Files(Username=Username)

                # messages_count = str(conut)

                # client.send(messages_count.encode(FORMAT))

                # if client.recv(16).decode() == "YES":

                    # client.send(Files.encode(FORMAT))



            elif Mode == "get_files":
                user = client.recv(128).decode()
                Files, conut, dates  = db.get_Files(Username=user)
                if conut != 0:
                    client.send(dates.encode(FORMAT))
                    client.send(Files.encode(FORMAT))
                else:
                    client.send("No messages".encode(FORMAT))
                    client.send("No messages".encode(FORMAT))
            elif Mode == "LOGIN":
                User = client.recv(128).decode().split("<sper>")
                client.send(self.login(User[0], User[1]).encode(FORMAT))

            elif Mode == "Register":
                User = client.recv(128).decode().split("<sper>")
                client.send(self.create_user(
                    User[0], User[1], User[2]).encode(FORMAT))

            Mode = client.recv(512)  # receive the optin mode from client
            Mode = Mode.decode(FORMAT)

        client.close()  # close the connetion between client and server

    def send_file(self, client, file_name, sender, username):
        file_path = db.get("SELECT path from Files WHERE name = ('{}') and path = ('{}') and Sender = ('{}')".format(username, "Server_files\\"+file_name, sender))
        sec_key = db.get(
            "SELECT session_key from Files WHERE Sender = ('{}') and name = ('{}') and path = ('{}')".format(sender, username, "Server_files\\"+file_name))
        with open(file_path, 'rb') as f:
            byte_read = f.read()

        # file size and session key
        client.send(("{}<sper>{}".format(
            len(byte_read), sec_key)).encode(FORMAT))
        client.send(byte_read)

        respones = client.recv(16).decode()
        if respones == 'OK':
            # delete file
            query = "DELETE FROM Files WHERE path = ('{}') and name = ('{}') and Sender = ('{}')".format(
                "Server_files\\"+file_name, username, sender)
            os.remove(file_path)
            os.remove(sec_key)
            db.delete(query)

    def receive_file(self, client, receiver):  # done
        pub = db.get(
            "SELECT Public_key from Public_Keys WHERE Uname = ('{}')".format(receiver))
        if pub == "False":
            client.send(" ".encode(FORMAT))
            
        else:
            client.send(pub.encode(FORMAT))
    

        file_name, file_size = client.recv(4096).decode().split("<SBER>")

        file_size = int(file_size)
        session_key = client.recv(64).decode()
        data = client.recv(file_size)

        path = 'Server_files\{}'.format(file_name)
        with open(path, 'wb') as f:
            f.write(data)

        return path, session_key

    def login(self, username, password):
        query = "SELECT Username from USERS WHERE Username = ('{}') and Password = ('{}')".format(
            username, password)
        if db.get(query) == username:
            return 'OK'
        else:
            return 'Fail'

    def create_user(self, username, password, key):
        User = "INSERT INTO USERS(Username,Password) VALUES('{}','{}')".format(
            username, password)
        public_key = "INSERT INTO Public_Keys(Uname,Public_Key) VALUES('{}','{}')".format(
            username, key)
        if db.add(User):
            db.add(public_key)
            return 'OK'
        else:
            return 'Fail'

    def Start(self):

        # create socket and defind the family and type of socket
        self.server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket with ip address and port number
        self.server_Socket.bind((self.HostIP, self.port))
        self.server_Socket.listen()  # start to listen to incoming connections

        print(
            f"[LISTENING] Server Start to listening\n")
        while True:
            client, address = self.server_Socket.accept()  # make connection establish
            print(
                f"[CONNECTION] connection establish {address[0]}:{address[1]}\n")

            # create a thread to handle a multi-connection
            thread = threading.Thread(
                target=self.handle_client, args=(client, address))
            thread.start()


Server = server("127.0.0.1", 5012)
Server.Start()
