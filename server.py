from flask import Flask, request, jsonify, abort
import time
from datetime import datetime 
from twilio.rest import TwilioRestClient
import postmates as pm

app = Flask(__name__)

class logic:
	def __init__(self):
		self.map = {}
		self.brd = {}
		sid = ""
		sec = ""

		self.twilio = TwilioRestClient(sid, sec)


	def update(self, json):
		# Calculates time difference. 
		def timeDiff(a, b):
			f = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
			return f(b) - f(a)

		def _cmp_delivery(d0, d1):
			d0_time = timeDiff(d0['start_time'], d0['end_time'])
			d1_time = timeDiff(d1['start_time'], d1['end_time'])
			return 1 if d0_time.total_seconds() - d1_time.total_seconds() > 0 else -1

		def _sub_delivery(d0, d1):
			d0_time = timeDiff(d0['start_time'], d0['end_time'])
			d1_time = timeDiff(d1['start_time'], d1['end_time'])
			return str(d0_time - d1_time)

		self.state = json
		if 'status' in json and json['status'] == 'pickup_complete':
			# Add start time. 
			self.map[json['delivery_id']] = {'start_time': json['created'], 'end_time': '', 'courier': json['data']['courier'], 'id':json['delivery_id'], 'points': [
                                {'point': {'latitude': json['data']['courier']['lat'], 'longitude': json['data']['courier']['lng'], 'timestamp': json['created']}}
]}
                elif json['delivery_id'] in self.map and 'status' in json and json['status'] == 'dropoff':
                        self.map[json['delivery_id']]['points'].append({'point':{'latitude': json['data']['courier']['lat'], 'longitude': json['data']['courier']['lng'], 'timestamp': json['created']}})
		elif 'status' in json and json['status'] == 'delivered':
			if json['delivery_id'] in self.map and self.map[json['delivery_id']]['end_time'] == '':
				# easier reference. 
				me = self.map[json['delivery_id']]
				# Add finish timestamp. 
				me['end_time'] = json['created']
				# Calculate Time Difference. 
				me['time'] = str(timeDiff(me['start_time'], 
					me['end_time']))
				# Add to leaderboard. 
				self.add(me)

				me = self.brd[me['courier']['name']]

				msg = me['best_effort']['courier']['name'] + ', '

				if me['best_effort']['id'] == json['delivery_id']:
					current_leader = self.current_leader()
					#print current_leader
					if current_leader['1']['best_effort']['courier']['name'] == me['best_effort']['courier']['name']:
						msg = msg + "you are the new leader! You set a record of " + current_leader['1']['best_effort']['time'] + '.\n'
					else:
						msg = msg + "you set a personal record! You are " + _sub_delivery(me['best_effort'], current_leader['1']['best_effort']) + " behind the current leader.\n"
				else:
					msg = msg + "you are " + _sub_delivery(me['best_effort'], self.map[json['delivery_id']]) + " behind your personal record. "
					# You set a new PR! You are x off from the leader. 
					# You are X off from your personal record. 
				phone_number = '3476337300'
				if not me['best_effort']['courier']['phone_number'] == '':
					phone_number = me['best_effort']['courier']['phone_number']
				message = self.twilio.messages.create(to='+1' + phone_number, from_="+16262437676", body=msg)

				print msg
				# TO DO: Twilio integration. 
				# Contant the driver with some info. 
				# Remove entry from live list. 
				del self.map[json['delivery_id']]
	
	# Adds an entry to the leader board. Saves multiple runs by rider. 
	def add(self, entry):
		def timeDiff(a, b):
			f = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
			return f(b) - f(a)

		def _cmp_delivery(d0, d1):
			d0_time = timeDiff(d0['start_time'], d0['end_time'])
			d1_time = timeDiff(d1['start_time'], d1['end_time'])
			return 1 if d0_time.total_seconds() - d1_time.total_seconds() > 0 else -1

		name = entry['courier']['name']
		# Add name if it's not in the leaderboard. 
		if not name in self.brd:
			self.brd[name] = {'best_effort': entry}
		elif _cmp_delivery(self.brd[name]['best_effort'], entry) > 0:
			self.brd[name] = entry
		else:
			# do nothing
			return

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

		for k, v in self.brd.iteritems():
			temp = temp + [{'name': k, 'best_effort': v['best_effort']}]

		for i in range (0, len(temp)):
			retVal.append({str(i + 1): sorted(temp, key = lambda e:  e['best_effort'], cmp = _cmp_delivery)[i]})
		return {'leaderboard':retVal}

	def current_leader(self):
		return self.ldrbrd()['leaderboard'][0]
			

	def json(self):
		return {'map': self.map, 'brd': self.brd}

	def jobs(self):
		return {'job': [k for k, _ in self.map.iteritems()]}

        def delall(self):
                self.map = {}
                self.brd = {}


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
	return jsonify(state.ldrbrd()), 200

@app.route('/jobs')
def jobs():
	return jsonify(state.jobs()), 200

@app.route('/deleteall', methods = ['DELETE'])
def deleteall():
        return jsonify(state.delall()), 200

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
