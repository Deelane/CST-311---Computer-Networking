
from socket import *
import _thread

#set alias
alias = input("Welcome to the chat server. Please enter an alias: ")

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

##Message Order##
#Server -> Client (Welcome message)
#Client -> Server (Send alias)
#Server -> Client (Confirm alias)
#Server -> Client (Confirm peer(s))


print("Hello, ", alias)
print("Waiting for chat partner...")

#accept the welcome message
#this also means we have one or more chat partners
#Server -> Client
message = clientSocket.recv(1024)
print("From Server: ", message.decode()) 

#send alias to server
#Client -> Server
clientSocket.send(alias.encode())

#Server confirms alias
#Server -> Client
message = clientSocket.recv(1024)
print("From Server: ", message.decode()) 

#Server confirms peer list
#Server -> Client
message = clientSocket.recv(1024)
print("From Server: ", message.decode()) 

###################
##Begin messaging##
###################
print("\nType a message and press enter to send. Enter 'quit' to quit. Enjoy your chat!")

hasSendThread = False
hasReceiveThread = False
chatting = True

def receive_Thread(clientSocket):
    
    #continuously poll and wait for messages
    while True:         
        #accept messages
        message = clientSocket.recv(1024)
        print(message.decode()) 

def send_Thread(clientSocket):

    #send messages
    while True:
        message = input()
        if (message.lower() == "bye"):
            print("Closing connection...")
            clientSocket.send(message.encode())
            chatting = False
            break
        else:
            print("You: ", message)
            clientSocket.send(message.encode())


while True:
    if (not hasSendThread):
        #one thread for sending one for receiving
        sendThread = _thread.start_new_thread(send_Thread, (clientSocket,))
        hasSendThread = True
        sendThread.join()
    if (not hasReceiveThread):
        receiveThread = _thread.start_new_thread(receive_Thread, (clientSocket,))
        hasReceiveThread = True
        receiveThread.join()
    if (not chatting):
        break
#close socket
print("Thank you for chatting!")
clientSocket.close()
print("Connection closed.")
