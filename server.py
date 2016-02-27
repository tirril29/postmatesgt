from flask import Flask, request, jsonify, abort
import time
import postmates as pm

app = Flask(__name__)

class logic:
	def __init__(self):
		self.state = {'data':'No data so far. '}
		self.map = {}
		self.ldr = {}

	def update(self, json):
		self.state = json
		if 'status' in json and json['status'] == 'pickup_complete':
			self.map[json['delivery_id']] = {'start_time': json['created'], 'end_time': '', 'courier': json['data']['courier']}
		elif 'status' in json and json['status'] == 'delivered':
			if json['delivery_id'] in self.map and self.map[json['delivery_id']['end_time'] == '':
				self.map[json['delivery_id']['end_time'] = json['created']]
		else:
			# do nothing
	
	def json(self):
		return self.map


state = logic()

'''
Routing
'''

@app.route('/')
def index():
	return 'hello world'

@app.route('/webhooks', methods = ['POST'])
def webhooks():
	if not request.json:
		abort(500)
	else:
		state.update(request.json)
		return jsonify({'value': 'success'}), 200

@app.route('/newest')
def newest():
	return jsonify(state.json()), 200

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
