import socket
from colorama import init , Fore
import threading
import database as db
init(convert=True)

FORMAT = "utf-8"
HEADERSIZE = 64

ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[5m'

class server(object):
    def __init__(self,HostIP,port):
        self.HostIP = HostIP
        self.port = port
       
    
    
    def handle_client(self,client,address):

        Mode = client.recv(512) # receive the option mode from client 
        Mode = Mode.decode(FORMAT) # convert from byte to string 
        
        connection = True
        while connection:
            if Mode == "Send_File": # receive message and send it back to  client in open mode
                

                Username = self.receive_data(client,address)
                url = self.receive_data(client,address).split("+")

                responese = db.add_File(Username=Username,File=url[0],Sender=[1])
                self.send_data(client,address,"The File is successfully sent")



            elif Mode == "Check_Messages":
                print("Check_Messages")
                Username = self.receive_data(client,address)
                print(Username)
                messages_count = db.get_File_count(Username)
                self.send_data(client,address,messages_count)
                if self.receive_data(client,address) == "Yes":
                    Files = db.get_File(Username=Username)
                    self.send_data(client,address,Files)


            elif Mode == "Quit_application":
                msg  = self.receive_data(client= client , address= address)
                self.send_data(client= client,address= address,msg= f"DISCONNECTED from {address[0]} ".upper())
                connection = False

            elif Mode == "LOGIN":
                User = self.receive_data(client,address).split("+")
                self.send_data(client,address,self.login(User[0],User[1]))
            

            elif Mode == "Register":
                User = self.receive_data(client,address).split("+")
                self.send_data(client,address,self.create_user(User[0],User[1]))

            Mode = client.recv(512) # receive the optin mode from client 
            Mode = Mode.decode(FORMAT)

        client.close() # close the connetion between client and server 


    def login(self,username,password):
        if db.Get_User(username,password):
            return 'OK'
        else:
            return 'Fail'
    
    
    def create_user(self,username,password):
        if db.Create_User(username,password):
            return 'OK'
        else:
            return 'Fail'
    

    def Start(self):

        self.server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# create socket and defind the family and type of socket 
        self.server_Socket.bind((self.HostIP, self.port)) # socket with ip address and port number 
        self.server_Socket.listen() # start to listen to incoming connections
        
        print(f"{UNDERLINE + BOLD}[LISTENING] Server Start to listening\n{ENDC}")
        while True:
            client , address = self.server_Socket.accept() # make connection establish
            print(f"{BOLD + Fore.GREEN}[CONNECTION] connection establish {address[0]}:{address[1]}{ENDC}\n")

            thread = threading.Thread(target= self.handle_client,args= (client,address)) # create a thread to handle a multi-connection
            thread.start()
            
    
    def send_data(self,client,address,msg):
        message = str(msg)
        message = f'{len(message):<{HEADERSIZE}}' + message # add the HEADERSIZE to the message
        print(f"{Fore.YELLOW + BOLD}[SENDING]send a message to {address[0]} : {msg}{ENDC}\n")
        client.send(message.encode(FORMAT))# send to client 


               
                
    def receive_data(self,client,address):
    
        full_message = ''
        new_msg = True
        while True:
            
            msg = client.recv(64) # receive message up to 64 bytes
            if new_msg: # if it a new message then 
                msg_length = int(msg[:HEADERSIZE]) # message lenght up to HEADERSIZE 
                new_msg = False
            full_message += msg.decode(FORMAT) # convet the received part of the message from byte to string
            
            if len(full_message) - HEADERSIZE == msg_length: # if the length of Full message - HEADERSIZE == message length then we received the whole message 
                print(f"{Fore.GREEN + BOLD}[RECEIVED] received message from {address[0]}:{full_message[HEADERSIZE:]}{ENDC}\n")
                new_msg = True
                message = full_message[HEADERSIZE:]
                full_message = ''
                return message
                

Server = server("127.0.0.1",5555)
Server.Start()
