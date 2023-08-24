from flask import Flask
from read_temp import read_temp
from read_height import read_height

app = Flask(__name__)

@app.route('/hello')
def home():
    return "HALO"


@app.route('/temp')
def temp():
    return f'{read_temp()}'

@app.route('/height')
def height():
    return f'{read_height()}'


app.run()