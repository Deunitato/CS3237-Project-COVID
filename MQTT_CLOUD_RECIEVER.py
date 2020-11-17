import paho.mqtt.client as mqtt
import numpy as np
import json
import time
import traceback
import requests
from MQTTDATA import Publisher


api_link  = 'http://52.221.218.172:5000/predict'
mqtt_pub = Publisher("test/moves", "18.140.67.252", 1883)

move_array = [None] * 3
counter = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        client.subscribe("test")
    else:
        print("Failed to connect")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        print(float(data['accelX']))
        processed_data = {"data":[float(data['accelX']), float(data['accelY']), float(data['accelZ']), float(data['gyroX']), float(data['gyroY']), float(data['gyroZ'])]}

        move = requests.post(api_link, json=processed_data)
        print("move :"  + str(move.text))

        '''
        if there is 3 same move and the time between current and the last send is more than 0.5s , then we send out a prediction
        '''

        # global move_array
        # global counter
        
        # move_to_publish = False

        # move_array[counter] = move.text['prediction']
        # counter += 1
        # if counter > 2:
        #     counter = 0

        # if move_array[1:] == move_array[:-1]:
        #     move_to_publish = move_array[0]

        # #TODO: add in publish to move topic
        # if move_to_publish != False:
        #     mqtt_pub.publish(str(move_to_publish))
        
        #TODO: add in publish to move topic
        mqtt_pub.publish(str(move.text))
        

    except:
        #traceback.print_exc()
        pass
    # TODO use the data.

def setup(hostname):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()
    return client

def main():
    client = setup("18.140.67.252")
    mqtt_pub.run()
    while True:
        pass

if __name__ == '__main__':
    main()
