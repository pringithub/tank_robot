# USAGE
# python3 streamer.py --ip 0.0.0.0 --port 8000

from flask import Response
from flask import Flask
from flask import render_template
import base64
import argparse
import zmq
import numpy as np


# initialize a flask object
app = Flask(__name__)


def setup_socket_sub(port):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind('tcp://*:{}'.format(port))
    socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
    return socket
IN_PORT=5555
socket = setup_socket_sub(IN_PORT)

def recv_frame(socket):
    frame = socket.recv_string()
    img = base64.b64decode(frame)
    #npimg = np.frombuffer(img, dtype=np.uint8)
    return img

def get_frame():
    encodedImage = recv_frame(socket)
    print('encodedImage received')
    # yield the output frame in the byte format
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
      bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
      # return the response generated along with the specific media
      # type (mime type)
      return Response(get_frame(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':

    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
                    threaded=True, use_reloader=False)
        
