from flask import Flask, render_template, redirect, url_for, request
from flask_apscheduler import APScheduler
import multiprocessing
import random

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



@app.route('/', methods=['GET', 'POST'])
def main():
    print(SKILLS)
    return render_template('monster_attack.html', Skills = SKILLS)

@app.route('/current-temperature')
def current_temperature():
    return '<meta http-equiv="refresh" content="1" /> Current temperature is ' + str(simulated.value), 200
 
@app.route('/pause-interval-task')
def pause_interval_task():
    scheduler.pause_job(id=INTERVAL_TASK_ID)
    return 'Interval task paused', 200
 
@app.route('/resume-interval-task')
def resume_interval_task():
    scheduler.resume_job(id=INTERVAL_TASK_ID)
    return 'Interval task resumed', 200
    
if __name__ == "__main__":
    app.run(debug=True)