from flask import Flask, request, jsonify, abort
import time
import postmates as pm
# import logic as l

app = Flask(__name__)

'''
Routing
'''

@app.route('/')
def index():
	return 'hello world'

@app.route('/webhooks')
def webhooks(request):
	print request.json
	return jsonify({'value': 'success'}), 201

if __name__ == '__main__':
	app.run(host='0.0.0.0')