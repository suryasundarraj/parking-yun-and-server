from pubnub import Pubnub
import json
import datetime
parkDAta = dict()
carPark = dict()
carMeter = dict()
pubnub = Pubnub(publish_key="pub-c-a1f796fb-1508-4c7e-9a28-9645035eee90", subscribe_key="sub-c-d4dd77a4-1e13-11e5-9dcf-0619f8945a4f")

def checking (requester,reqtype,deviceid,requestval):
	l_carNum = requestval
	if (requester == "APP"):
		if (reqtype == 1):
			pubnub.publish(channel='parkingapp-resp', message=parkDAta)
			print "Sent OK"
		elif (reqtype == 2):
			carMeter[l_carNum] = [deviceid,0,0,0]
			if(carMeter.has_key(l_carNum)):
				l_startTime = datetime.datetime.now()
				l_dateStr = str(l_startTime.day) + "." + str(l_startTime.month) + "." + str(l_startTime.year)
				l_stimeStr = str(l_startTime.hour) + ":" + str(l_startTime.minute) + ":" + str(l_startTime.second)
				l_parsedDate = datetime.datetime.strptime(l_dateStr,'%d.%m.%Y').strftime('%m-%d-%Y')
				l_parsedStartTime = datetime.datetime.strptime(l_stimeStr,'%H:%M:%S').strftime('%H:%M:%S')
				carMeter[l_carNum][1] = l_startTime
				carPark["sessionType"] = 0
				carPark["carNum"] = l_carNum
				carPark["lotNumber"] = deviceid
				carPark["parkingDate"] = l_parsedDate
				carPark["startTime"] = l_parsedStartTime
				carPark["endTime"] = 0
				carPark["totalTime"] = 0
				carPark["totalAmt"] = 0
				pubnub.publish(channel=l_carNum, message=carPark)
				parkDAta[deviceid] = 1
				pubnub.publish(channel='parkingapp-resp', message=parkDAta)
			else:
				print "CAR NOT PARKED SUCCESSFULLY"

		elif (reqtype == 3):
			if(carMeter.has_key(l_carNum)):
				l_endTime = datetime.datetime.now()
				carMeter[l_carNum][2] = l_endTime
				l_etimeStr = str(l_endTime.hour) + ":" + str(l_endTime.minute) + ":" + str(l_endTime.second)
				l_parsedEndTime = datetime.datetime.strptime(l_etimeStr,'%H:%M:%S').strftime('%H:%M:%S')
				carPark["sessionType"] = 1
				carPark["carNum"] = l_carNum
				carPark["lotNumber"] = deviceid
				carPark["endTime"] = l_parsedEndTime
				totalTime = carMeter[l_carNum][2] - carMeter[l_carNum][1]
				l_totalMin = divmod(totalTime.days * 86400 + totalTime.seconds, 60)[0]
				carPark["totalTime"] = l_totalMin
				if(l_totalMin < 60):
					carPark["totalAmt"] = 20
				elif(l_totalMin > 60 and l_totalMin < 120):
					carPark["totalAmt"] = 40
				elif(l_totalMin > 120 and l_totalMin < 180):
					carPark["totalAmt"] = 60
				elif(l_totalMin > 180 and l_totalMin < 240):
					carPark["totalAmt"] = 80
				elif(l_totalMin > 240 and l_totalMin < 300):
					carPark["totalAmt"] = 100
				elif(l_totalMin > 300 and l_totalMin < 360):
					carPark["totalAmt"] = 120
				elif(l_totalMin > 360 and l_totalMin < 420):
					carPark["totalAmt"] = 140
				elif(l_totalMin > 420 and l_totalMin < 480):
					carPark["totalAmt"] = 160
				elif(l_totalMin > 480 and l_totalMin < 540):
					carPark["totalAmt"] = 180
				elif(l_totalMin > 540 and l_totalMin < 600):
					carPark["totalAmt"] = 200
				elif(l_totalMin > 600 and l_totalMin < 660):
					carPark["totalAmt"] = 220
				elif(l_totalMin > 660 and l_totalMin < 720):
					carPark["totalAmt"] = 240
				print pubnub.publish(channel=l_carNum, message=carPark)
				del carMeter[l_carNum]
			else:
				print "ERROR CAR NUMBER"
	
def callback(message, channel):
	parkDAta.update(message)
	pubnub.publish(channel='parkingapp-resp', message=message)
	print parkDAta

def appcallback(message, channel):
	print message
	requester = message["requester"]
	deviceid = message["deviceID"]
	reqtype = message["requestType"]
	requestval = message["requestValue"]
	checking(requester,reqtype,deviceid,requestval)
         
def error(message):
    print("ERROR : " + str(message))
   
def reconnect(message):
    print("RECONNECTED")
  
def disconnect(message):
    print("DISCONNECTED")

pubnub.subscribe(channels='parkingdevice-resp', callback=callback, error=callback,
                 reconnect=reconnect, disconnect=disconnect)

pubnub.subscribe(channels='parkingapp-req', callback=appcallback, error=appcallback,
                 reconnect=reconnect, disconnect=disconnect)
