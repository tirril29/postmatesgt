from flask import Flask, request, jsonify, abort
import time
from datetime import datetime 
import twilio
import postmates as pm

app = Flask(__name__)

class logic:
	def __init__(self):
		self.state = {'data':'No data so far. '}
		self.map = {}
		self.brd = {}

	def update(self, json):
		# Calculates time difference. 
		def timeDiff(a, b):
			f = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
			return f(b) - f(a)

		self.state = json
		if 'status' in json and json['status'] == 'pickup_complete':
			# Add start time. 
			self.map[json['delivery_id']] = {'start_time': json['created'], 'end_time': '', 'courier': json['data']['courier']}
		elif 'status' in json and json['status'] == 'delivered':
			if json['delivery_id'] in self.map and self.map[json['delivery_id']]['end_time'] == '':
				# Add finish timestamp. 
				self.map[json['delivery_id']]['end_time'] = json['created']
				# Calculate Time Difference. 
				self.map[json['delivery_id']]['time'] = str(timeDiff(self.map[json['delivery_id']]['start_time'], 
					self.map[json['delivery_id']]['end_time']))
				# Add to leaderboard. 
				self.add(self.map[json['delivery_id']])
				# TO DO: Twilio integration. 
				# Contant the driver with some info. 
				# Remove entry from live list. 
				del self.map[json['delivery_id']]
	
	# Adds an entry to the leader board. Saves multiple runs by rider. 
	def add(self, entry):
		name = entry['courier']['name']
		# Add name if it's not in the leaderboard. 
		if not name in self.brd:
			self.brd[name] = []
		self.brd[name].append(entry)

	def ldrbrd(self):
		def timeDiff(a, b):
			f = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
			return f(b) - f(a)

		def _cmp_delivery(d0, d1):
			d0_time = timeDiff(d0['start_time'], d0['end_time'])
			d1_time = timeDiff(d1['start_time'], d1['end_time'])
			return 1 if d0_time.total_seconds() - d1_time.total_seconds() > 0 else -1

		retVal = []
		temp = []

		if not self.brd == {}:
			for courier, deliveries in self.brd.iteritems():
				temp = temp + [{'name': courier, 'delivery': sorted(deliveries, _cmp_delivery)[0]}]
				for i in range(0, len(temp)):
					retVal.append({i + 1: sorted(temp, 
						key = lambda e:  e['delivery'], 
						cmp = _cmp_delivery)[i]})
			return retVal
		else:
			return {}
			

	def json(self):
		return {'map': self.map, 'brd': self.brd}


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

@app.route('/leaders')
def leaders():
	return jsonify(state.ldrbrd()[:10])

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
