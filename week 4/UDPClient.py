import time
from socket import *
serverName = '127.0.0.1' #localhost
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
#1 second timeout
clientSocket.settimeout(1)

#amount of times to ping server
pings = 10

#Track number of packets sent
#Pack loss rate is packetsSent / packetLoss
packetsSent = 0
packetsReceived = 0

alpha = 0.125 
beta = 0.25
sampleRTT = 0 #milliseconds
estimatedRTT = 0 #milliseconds
devRTT = 0 #milliseconds
timeoutInterval = 60000 #milliseconds

minRTT = 0
maxRTT = 0
sumRTT = 0

for i in range(pings):    

    #create and send message
    message = "ping " + str(i + 1)
    print("\nSending message [", message, "] to " + "[" + serverName + "]: " + str(serverPort) + "...")
    sentTime = time.time()
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    
    #wait 1 second for response
    try:
        returnMessage, serverAddress = clientSocket.recvfrom(2048)
    #packet loss
    except timeout: #for some reason timeout exception wont work here, so we use OSError which is a parent class
        print("-No response from server-")
        print(message + " request timed out\n")
    #response received
    else:
        #packet received
        packetsReceived += 1
    
        #calculate RTT
        receivedTime = time.time()
        elapsedTime = (receivedTime - sentTime) * 1000
        
        #if it's the first ping we sent
        if (packetsSent == 0):
            minRTT = maxRTT = sumRTT = estimatedRTT = sampleRTT = elapsedTime
            devRTT = sampleRTT / 2
        #not the first ping sent
        else:
            if (elapsedTime < minRTT): #update minRTT 
                minRTT = elapsedTime
            if (elapsedTime > maxRTT): #update maxRTT 
                maxRTT = elapsedTime
            sumRTT += elapsedTime #update sum
            sampleRTT = elapsedTime
            estimatedRTT = (1 - alpha) * estimatedRTT + (alpha * sampleRTT)
            devRTT = (1 - beta) * devRTT + (beta * abs(sampleRTT - estimatedRTT))
            timeoutInterval = estimatedRTT + (4 * devRTT)
            
        print("Reply from: ", serverAddress, "time =",elapsedTime, "ms")    
        print("Message: [", returnMessage, "]")

            
        
    #increment packet count
    packetsSent+=1 
    
#close socket    
clientSocket.close()

##calculate RTT values

avgRTT = sumRTT / packetsReceived

packetsLost = packetsSent - packetsReceived
percentLost = (packetsLost / packetsSent) * 100

##display data
print("\n\nPackets:")
print("  Sent =", packetsSent)
print("  Received =", packetsReceived)
print("  Lost =", packetsLost, "(", percentLost, "% Loss)")
print("\n\nApproximate Round Trip Times (RTT):")
print("  Minimum =", minRTT, "ms")
print("  Maximum =", maxRTT, "ms")
print("  Average =", avgRTT, "ms")
print("\nEstimatedRTT =", estimatedRTT, "ms")
print("DevRTT =", devRTT, "ms")
print("Timeout Interval =", timeoutInterval, "ms")

