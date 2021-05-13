import rahultest as util
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
io = SocketIO(app)


@app.route('/')
def start():
    return render_template('index.html')

@io.on('connect')
def test_connect():
    io.emit('after connect', "connection Successful")

@io.on('newFrame')
def process_frame(raw_frame):
    img = util.convert_uri(raw_frame)
    lined_img = util.canvas(img)
    url = util.convert_img(lined_img)
    io.emit('disp_img', url)


if __name__ == '__main__':
    io.run(app, host = '0.0.0.0')