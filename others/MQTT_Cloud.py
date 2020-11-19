import requests
import time
import json
from MQTTDATA import Subscriber
from MQTTDATA import Publisher
from apscheduler.schedulers.background import BackgroundScheduler

mqtt_sub = Subscriber("test", "18.140.67.252", 1883)
mqtt_pub = Publisher("test/moves", "18.140.67.252", 1883)
scheduler = BackgroundScheduler()
if not scheduler.running: 
    scheduler.start()
scheduler.add_job(mqtt_sub.run, 'date')
DATA = 1
def getData():
    global DATA
    DATA = mqtt_sub.getData()
scheduler.add_job(id="collect_data", func=getData, trigger='interval', seconds=2)




# scheduler.add_job(getData, 'interval', seconds=1)

def getPrediction():
    global DATA
    raw_data = DATA
    print("Raw:" + str(raw_data) + "\n")

    if raw_data == 1:
        return
    try:
        data = json.loads(str(raw_data))
    except TypeError as e:
        print(e.with_traceback)
    
    print("data:" + str(data) + "\n")

    #process data
    processed_data = [data['accelX'], data['accelY'], data['accelZ'], data['gyroX'], data['gyroY'], data['gyroZ']]
    #print(processed_data)

    api_link  = 'http://52.221.218.172:5000/predict'
    r = requests.post(url = api_link, data = processed_data)
    move = requests.get(url = api_link)
    mqtt_pub.publish(str(move.json()))
    print("move:", str(move.json()))

if __name__ == "__main__":
    

    # Listener
    
    mqtt_pub.run()
    try:
        while True:
            getPrediction()
    except Exception as e:
        print(e.with_traceback)
        #scheduler.shutdown()

