import paho.mqtt.client as mqtt

class Subscriber:
    def __init__(self, topic, ip, port, username, password):
        self.MQTT_DATA = 1
        self.client = mqtt.Client()
        self.client.username_pw_set(username = username, password = password)
        self.topic = topic
        self.ip = ip
        self.port = port
        # self.username = username
        # self.password = password


    def on_connect(self, client, userdata, flags,rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        self.MQTT_DATA = str(msg.payload.decode('ascii'))
        #print(self.MQTT_DATA)
        #print(msg.topic + " " + str(msg.payload.decode('ascii')))

    def getData(self):
        return self.MQTT_DATA

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        print("Connecting")
        self.client.connect(self.ip, self.port, 60)
        
        #self.client.tls_set("ca.pem", "client.crt", "client.key")
        self.client.loop_forever()

# mqtt = MQTTDATA()
# mqtt.run()
#print(mqtt.getData())

class Publisher:
    def __init__(self, topic, ip, port, username, password):
        self.client = mqtt.Client()
        self.client.username_pw_set(username = username, password = password)
        self.topic = topic
        self.ip = ip
        self.port = port
        # self.username = username
        # self.password = password

    def on_connect(self, client, userdata, flags,rc):
        print("Connected with result code " + str(rc))

    def publish(self, data):
        print("Sending messsage")
        self.client.publish(self.topic, data)

    def run(self):
        
        self.client.on_connect = self.on_connect
        print("Connecting")
        self.client.connect(self.ip, self.port, 60)
        
        #self.client.tls_set("ca.pem", "client.crt", "client.key")
        # self.client.loop_forever()
