import paho.mqtt.client as mqtt

class Subscriber:
    def __init__(self):
        self.MQTT_DATA = 1
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags,rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe("test/charlotte")
    def on_message(self, client, userdata, msg):
        self.MQTT_DATA = str(msg.payload.decode('ascii'))
        print(self.MQTT_DATA)
        #print(msg.topic + " " + str(msg.payload.decode('ascii')))

    def getData(self):
        return self.MQTT_DATA

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        print("Connecting")
        self.client.connect("18.140.67.252", 1883, 60)
        self.client.loop_forever()

# mqtt = MQTTDATA()
# mqtt.run()
#print(mqtt.getData())