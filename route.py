from flask import Flask, render_template
# from flask_socketio import SocketIO, emit


''''
export FLASK_APP=route.py
export FLASK_ENV=development
flask run --host 0.0.0.0
'''

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('first_figure.html')