from MQTTDATA import Publisher
import json
import random


import time


def main():
    mqtt_pub = Publisher("data/moves", "18.140.67.252", 1883, "charlotte", "charlotteiscool")
    mqtt_pub.run()
    counter = 0
    moves = ["stable", "stab", "magic", "shield", "buff", "slash", "surrender"]
    while True:
        playerno = random.randint(1,2)
        movesno = random.randint(0,6)
        data = {"player": playerno, "prediction": moves[movesno]}
        mqtt_pub.publish(json.dumps(data))
        counter = counter + 1
        time.sleep(0.2)

if __name__ == '__main__':
    main()