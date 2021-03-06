from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_apscheduler import APScheduler
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import multiprocessing
import random
import sys
import paho.mqtt.client as mqtt
from MQTTDATA import Subscriber

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
if not scheduler.running: 
    scheduler.start()

INTERVAL_TASK_ID = 'interval-task-id'

SKILLS = {"Slash" : True, "Shield": True}


"""
MQTT STUFF
"""
mqtt = Subscriber("data/moves", "18.140.67.252", 1883,"charlotte", "charlotteiscool")

scheduler.add_job(id="data_id", func=mqtt.run, trigger='date')
MQTT_DATA = {}
def getData():
    global MQTT_DATA
    MQTT_DATA = mqtt.getData()
scheduler.add_job(id="collect_data", func=getData, trigger='interval', seconds=0.1)





"""
Flask stuff
"""
prevData = {"prediction": "stable"}
counter = 0
@app.route('/', methods=['GET', 'POST'])
def main():
    print(SKILLS)
    return render_template('monster.html')

@app.route('/death', methods=['GET', 'POST'])
def death():
    return render_template('death.html')
    
@app.route('/getdata', methods=['GET', 'POST'])
def jsondata():
    global prevData
    global counter
    default = '{"prediction": "stable"}'
    print(default)
    
    if("stable" not in MQTT_DATA and MQTT_DATA == prevData and counter < 6):
        counter = counter + 1
        return jsonify(default)
    prevData = MQTT_DATA
    counter = 0

    return jsonify(MQTT_DATA)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    return render_template('graph.html')

    
if __name__ == "__main__":
    #socketio.run(app, host='localhost', port=5000, use_reloader=True, debug=True)
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        scheduler.shutdown(wait=True)
        sys.exit()

