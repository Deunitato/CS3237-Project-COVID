from flask import Flask, render_template, redirect, url_for, request
from flask_apscheduler import APScheduler
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import multiprocessing
import random
import paho.mqtt.client as mqtt
from MQTTDATA import Subscriber

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


INTERVAL_TASK_ID = 'interval-task-id'

SKILLS = {"Slash" : True, "Shield": True}

#For simulation 
simulated = multiprocessing.Value('d', 29)
def interval_task():
    simulated.value = random.randint(1, 100)
    if (simulated.value % 2) == 0:
        SKILLS["Slash"]  = True
    else: 
        SKILLS["Slash"]  = False

scheduler.add_job(id=INTERVAL_TASK_ID, func=interval_task, trigger='interval', seconds=1)


"""
MQTT STUFF
"""
mqtt = Subscriber()
scheduler.add_job(id="data_id", func=mqtt.run, trigger='date')
MQTT_DATA = {}
def getData():
    global MQTT_DATA
    MQTT_DATA = mqtt.getData()

scheduler.add_job(id="another", func=getData, trigger='interval', seconds=1)




"""
Flask stuff
"""

@app.route('/', methods=['GET', 'POST'])
def main():
    print(SKILLS)
    return render_template('monster_attack.html', Skills = SKILLS)

@app.route('/data', methods=['GET', 'POST'])
def index():
    return render_template('viewdata.html', data = MQTT_DATA)

    
if __name__ == "__main__":
    #socketio.run(app, host='localhost', port=5000, use_reloader=True, debug=True)
    app.run(debug=True)

