from socket import *
import threading
import _thread

#thread counter in the form of a lock
class thread_Counter(object):
  
    def __init__(self, count = 0):
        self.lock = threading.Lock()
        self.counter = count
    
    #increment function
    def increment(self):
        #acquire lock
        self.lock.acquire()
        try:
            self.counter += 1
        #release lock
        finally:
            self.lock.release()
                #increment function
                
    def decrement(self):
        #acquire lock
        self.lock.acquire()
        try:
            self.counter -= 1
        #release lock
        finally:
            self.lock.release()

serverPort = 12000

#initialize TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

connections = []
clientX = ""
clientY = ""

#attempt to bind socket to port
try:
    serverSocket.bind(('',serverPort))
except socket.error as exception:
    print(str(exception))
    
#wait for connections
serverSocket.listen(5)
print("\nThe server is ready to receive")


#initialize thread counter
threadCounter = thread_Counter()

def client_thread(client):
    print("Thread created for client")

    #class is self locking so we can just call increment here
    threadCounter.increment()
    
    print("Total live threads:", threadCounter.counter)
    
    #Welcome message
    client.send(str.encode("Connected to server"))

    while True:
        if (threadCounter.counter == 2):
        
            sentence = client.recv(1024).decode()
            capitalizedSentence = sentence.upper()
            client.send(capitalizedSentence.encode())
            
            #let the client receive the message "QUIT" first before breaking so the client connection will close
            if sentence == "quit":
                break
    client.close()
    threadCounter.decrement()

    print("Client connection closed")
    print("Client thread finished\n")
    print("New live thread count:", threadCounter.counter)

        
while True:
    
    #accept new connections
    connectionSocket, addr = serverSocket.accept()
    print("\n\nAccepted new connection.\n")
    print("User", addr, " connected.")

    connections.append(addr)
    if (len(connections) == 2):
        clientX = str(connections[0])
        clientY = str(connections[1])
        print("Client X: ", clientX)
        print("Client Y: ", clientY)
        
    #create new thread for connection
    #pass client_thread object and new connection to thread
    try:
        clientThread = _thread.start_new_thread(client_thread, (connectionSocket,))

    except OSError as e:
        print(e)
#close connection
connectionSocket.close()