import paho.mqtt.client as mqtt
import numpy as np
import json
import time
import traceback

file_number = 0
file_name   = 'demo/char_stab.json'
#file_name_number = file_name.format(file_number)
f = open(file_name, "a")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        client.subscribe("test/charlotte")
    else:
        print("Failed to connect")

def on_message(client, userdata, msg):
#    global file_number, file_name, f
    try:
        data = json.loads(msg.payload)
        '''
        temp = file_number
        if "key1" in data and data["key1"] == 1:
            file_number = file_number + 1
        if "key2" in data and data["key2"] == 1:
            file_number = file_number + 1
        if file_number > temp:
            f.close()
            file_name_number = file_name.format(file_number)
            f = open(file_name_number, "a")
        '''
        data['time'] = int(round(time.time()*1000))
        print(data)
        f.write(json.dumps(data))
        f.write("\n")
    except:
        traceback.print_exc()
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
    while True:
        pass

if __name__ == '__main__':
    main()
