from flask import Flask
from flask_cors import CORS, cross_origin
from read_temp import read_temp
from read_height import read_height, read_height_init
from read_max30100 import read_max30100, has_hand
from read_weight import read_weight, read_weight_init
import RPi.GPIO as GPIO
from signal import SIGINT, signal, SIGTERM, SIGHUP
from constants import STATE

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

state = STATE.IDLE


def main():
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    signal(SIGINT, safe_exit)

    app.run()

def safe_exit(signum, frame):
    print("Closing app server cleanly..")

    if state == STATE.WEIGHT_INIT or state == STATE.WEIGHT:
        try:
            GPIO.cleanup() 
        except:
            print("GPIO cleanup failed")

    exit(0)

@app.route('/hello')
@cross_origin()
def home():
    return "HALO"


@app.route('/weight_init')
@cross_origin()
def weight_init():
    global state

    state = STATE.WEIGHT_INIT
    weight_init = read_weight_init()
    state = STATE.IDLE
    return f'{weight_init}'

@app.route('/weight')
@cross_origin()
def weight():
    global state
    state = STATE.WEIGHT
    weight = read_weight()
    state = STATE.IDLE
    return f'{weight}'


@app.route('/height_init')
@cross_origin()
def height_init():
    global state
    state = STATE.HEIGHT_INIT
    height_init = read_height_init()
    state = STATE.IDLE
    return f'{height_init}'

@app.route('/height')
@cross_origin()
def height():
    global state
    state = STATE.HEIGHT
    height = read_height()
    state = STATE.IDLE
    return f'{height}'


@app.route('/vitals_init')
@cross_origin()
def vitals_init():
    # temp, pulse, spo2
    global state
    state = STATE.VITALS_INIT
    vitals_init = has_hand()
    state = STATE.IDLE
    return f'{vitals_init}'

@app.route('/vitals')
@cross_origin()
def vitals():
    # temp, pulse, spo2
    global state
    state = STATE.VITALS
    temp, (pulse, spo2) = read_temp(), read_max30100()
    state = STATE.IDLE
    return f'{temp} {pulse} {spo2}'





if __name__ == '__main__':
    main()