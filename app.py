from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('monster_attack.html')

    
if __name__ == "__main__":
    app.run(debug=True)