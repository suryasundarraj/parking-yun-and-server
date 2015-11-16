from pubnub import Pubnub
import datetime
import threading
import multiprocessing as mp
import sys

userData = dict()
myCar = dict()
pubnub = Pubnub(publish_key="pub-c-a1f796fb-1508-4c7e-9a28-9645035eee90", subscribe_key="sub-c-d4dd77a4-1e13-11e5-9dcf-0619f8945a4f")

def callback(message, channel):
	userData.update(message)

def caRcallback(message, channel):
	myCar.update(message)

def dataHandling(stdin):
		l_action = int(stdin.readline().strip())
		if(l_action == 1):
			pubnub.publish(channel='parkingapp-req', message={"requester":"APP","deviceID":0,"requestType":1,"requestValue":0})
		elif(l_action == 2):
			pubnub.publish(channel='parkingapp-req', message={"requester":"APP","deviceID":"001","requestType":2,"requestValue":"KA01M5512"})
		elif(l_action == 3):
			pubnub.publish(channel='parkingapp-req', message={"requester":"APP","deviceID":"001","requestType":3,"requestValue":"KA01M5512"})
		elif(l_action == 4):
			print "\n\n", userData
			print "\n\n", myCar
			
def error(message):
    print("ERROR : " + str(message))
  
def connect(message):
    print "CONNECTED"
  
def reconnect(message):
	print("RECONNECTED")
  
def disconnect(message):
	print("DISCONNECTED")

pubnub.subscribe(channels='parkingapp-resp', callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)
pubnub.subscribe(channels='KA01M5512', callback=caRcallback, error=caRcallback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)

if __name__ == '__main__':
	while True:
		t1 = threading.Thread(target=dataHandling, args=(sys.stdin,))
		t1.start()
		t1.join()
	