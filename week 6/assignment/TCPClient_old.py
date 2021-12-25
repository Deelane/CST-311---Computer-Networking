from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

print(clientSocket.getsockname())
#brute force accept the welcome message
modifiedSentence = clientSocket.recv(1024)
if modifiedSentence:
    print("From Server: ", modifiedSentence.decode()) 

sentence = ""
while True:
    sentence = input('Input lowercase sentence:')
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    message = modifiedSentence.decode()
    print("From Server: ", message) 
    if (message == "QUIT"):
        print("Closing connection")
        break

clientSocket.close()
print("Connection closed")