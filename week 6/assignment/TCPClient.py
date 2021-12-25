from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

print(clientSocket.getsockname())

#brute force accept the welcome message
message = clientSocket.recv(1024)

#if message is not null
if message:
    print("From Server: ", message.decode()) 

#send initial message
sentence = input('Send a message:')
clientSocket.send(sentence.encode())

#don't send anymore messages
#just let server send messages until quittin' time
while True:
    message = clientSocket.recv(1024)
    if message:
        if (message.decode() == "quit"):
            print("Closing connection...")
            break
        else:
            print("From Server: ", message.decode()) 

clientSocket.close()
print("Connection closed.")