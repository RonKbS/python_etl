from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from live_tweets import *


# export FLASK_APP=route.py
# export FLASK_ENV=development


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')