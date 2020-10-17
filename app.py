from flask import Flask, render_template, redirect, url_for, request
from flask_apscheduler import APScheduler

app = Flask(__name__)

SKILLS = {"Slash" : True, "Shield": True}

@app.route('/', methods=['GET', 'POST'])
def main():
    print(SKILLS)
    return render_template('monster_attack.html', Skills = SKILLS)

    
if __name__ == "__main__":
    app.run(debug=True)