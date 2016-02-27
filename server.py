from flask import Flask, request, jsonify, abort
import time

app = Flask(__name__)

'''
Routing
'''

@app.route('/')
def index():
	return 'hello world'

if __name__ == '__main__':
	app.run(host='0.0.0.0')