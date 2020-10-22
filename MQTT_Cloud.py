import requests
import time
from MQTTDATA import Subscriber
from MQTTDATA import Publisher

mqtt_sub = Subscriber("test/charlotte", "18.140.67.252", 1883)
mqtt_pub = Publisher("test/moves", "18.140.67.252", 1883)

def getPrediction():
    # data = mqtt_sub.getData()
    data = {'hello':'hello'}
    dummy_api_link  = 'https://jsonplaceholder.typicode.com'
    r = requests.post(url = dummy_api_link+"/posts", data = data)
    move = requests.get(url = dummy_api_link+"/posts/1")
    mqtt_pub.publish(str(move.json()))

if __name__ == "__main__":

    # Listener
    # mqtt_sub.run()
    mqtt_pub.run()

    while True:
        getPrediction()
        time.sleep(5)
