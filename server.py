<<<<<<< HEAD
#!/usr/bin/env python

import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
app = Flask(__name__)
socketio = SocketIO(app)
id_list = []

@socketio.on('connect')
def on_connect():
    # print(request)
    client_id = request.args['id']
    id_list.append(client_id)
    print(client_id, 'connected !')
    # broadcast
    socketio.emit('get_id_list', {'id_list': id_list})


@socketio.on('_disconnect')
def dis_connect(message):
    client_id = message['id']
    id_list.remove(client_id)
    print(client_id, 'disconnected !')
    # broadcast
    socketio.emit('get_id_list', {'id_list': id_list})

@socketio.on('message')
def handle_message(message):
    print('handle_message')
    print('message', message) 
    send(message)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=3000)
=======
import os
import base64
from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
import requests
from flask_cors import CORS

app = Flask(__name__, static_folder='build')
CORS(app)
socket = SocketIO(app)

img_file = None
img_string = ''

@socket.on('connect')
def on_connect():
	print ("User connected!")

@app.route("/api", methods=["POST"])
def decode():
	global img_file
	img_file = request.files['webcam']
	# img_string = base64.b64encode(img_file.read()) # base64 is larger
	img_string = img_file.read()
	# print (img_string)
	# print (type(img_string))
	socket.emit('get_image', {'image_data': img_string})
	return "POST received!"

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def render(path):
	print (path)
	if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
		return send_from_directory(app.static_folder, path)
	else:
		return send_from_directory(app.static_folder, 'index.html')

	

if __name__ == "__main__":
	app.run()
>>>>>>> 037aac062b46fdb6b6a454f7562d675534102207
