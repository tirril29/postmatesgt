from flask import Flask, request, jsonify, abort
import time
import postmates as pm

app = Flask(__name__)

update = ""

'''
Routing
'''

@app.route('/')
def index():
	return 'hello world'

@app.route('/webhooks', methods = ['POST'])
def webhooks(request):
	update = request.json
	return jsonify({'value': 'success'}), 201

@app.route('/newest')
def newest():
	return update

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
	app.run(host='0.0.0.0')