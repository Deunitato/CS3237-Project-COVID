import paho.mqtt.client as mqtt
import numpy as np
import json
import time
import traceback
import requests
import threading
import concurrent.futures
import random

from MQTTDATA import Publisher


api_link  = 'http://52.221.218.172:5000/predict'
mqtt_pub = Publisher("test/moves", "18.140.67.252", 1883, "charlotte", "charlotteiscool")

move_buffer = [None] * 3
counter = 0

def random_moves():
    moves = ['stable', 'slash', 'stab']
    random_move = random.randint(0, 2)
    return moves[random_move]

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

        # Get prediction
        move = requests.post(api_link, json=processed_data)
        print("move :"  + str(move.text))

       
        # move = random_moves()
        # print("Move: " + str(move) + "\n")

        '''
        if there is 3 same move and the time between current and the last send is more than 0.5s , then we send out a prediction
        '''

        '''
        Works by constantly adding into buffer of size 3 and checking if all is a slash or all is a stab, 
        and sends the result to MQTT

        - if stable, it'll continue
        - else it will sleep for 0.5s
        '''

        # move_array[counter] = str(move.text)
        global move_buffer
        global counter

        move_buffer[counter] = move
        counter = counter + 1

        if(counter == 3):
            counter = 0

        print(move_buffer)

        # Sleeps if sees consecutive values
        if(move_buffer[:-1] == move_buffer[1:] and move_buffer[0] != 'stable'):
            print("3 moves")
            jsondict = {"prediction" : move_buffer[0]}
            mqtt_pub.publish(json.dumps(jsondict))
            # mqtt_pub.publish(json.dumps(jsondict))
            # mqtt_pub.publish(json.dumps(jsondict))
            jsondict = {"prediction" : "stable"}
            mqtt_pub.publish(json.dumps(jsondict))
        else:
            jsondict = {"prediction" : "stable"}
            mqtt_pub.publish(json.dumps(jsondict))

    except:
        #traceback.print_exc()
        pass

def setup(hostname):
    
    client = mqtt.Client()
    client.username_pw_set("charlotte", "charlotteiscool")
    #client.tls_set("ca.pem", "client.crt", "client.key")
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
