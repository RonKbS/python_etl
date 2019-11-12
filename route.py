from flask import Flask, render_template
# from flask_socketio import SocketIO, emit


''''
export FLASK_APP=route.py
export FLASK_ENV=development
flask run --host 0.0.0.0 || python route.py
'''

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('first_figure.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)
