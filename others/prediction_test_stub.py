from MQTTDATA import Publisher

import time

def main():
    mqtt_pub = Publisher("test", "18.140.67.252", 1883)
    mqtt_pub.run()
    counter = 0
    while True:
        mqtt_pub.publish(counter)
        counter = counter + 1
        time.sleep(0.2)

if __name__ == '__main__':
    main()