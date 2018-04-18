#!flask/bin/python
from flask import Flask, json, jsonify, make_response, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from urllib.parse import urlparse

from pprint import pprint
import json, requests
import ast

from _utils import *
from _parsePing import marvinPingParser
from marvin_config import *

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[limitValue()],
)


puppeteer = 'http://' + puppeteerValues("host") + ':' + str(puppeteerValues("port"))

@app.route('/')
def root():
	return('Welcome')

@app.route('/info')
@limiter.exempt
def getInfo(): # This shouldn't be static anymore
	return(infoValues()), 200

@app.route('/ping/', methods = ["GET","POST"])
@app.route('/ping/<hostname>', methods = ["GET","POST"])
#@limiter.limit(limitValue())
def ping(hostname):
	if request.method == 'POST':
		data = ping_options()

		cmd = '-c%s -n -s%s -M%s'% (data['count'] , data['size'] , data['pmtu'])
		
		output = runPing(['ping', cmd , punyHostname(hostname)])
		
		result = marvinPingParser(hostname, data, output)
		
		pprint(output)
		
		return(json.dumps(result, indent=4)),200
		
	else:
		return('Method not allowed!'), 400

@app.route('/ping6/', methods = ["GET","POST"])
@app.route('/ping6/<hostname>', methods = ["GET","POST"])
#@limiter.limit(limitValue())
def ping6(hostname):
	if request.method == 'POST':
		data = ping_options()

		cmd = '-c%s -n -s%s -M%s'% (data['count'] , data['size'] , data['pmtu'])
		output = runPing(['ping6', cmd , punyHostname(hostname)])
		
		result = marvinPingParser(hostname, data, output)
		
		pprint(output)

		pprint('ping6 %s %s' %(cmd, hostname))
		
		return(json.dumps(result, indent=4)),200
	else:
		return('Method not allowed!'), 400

@app.route('/request/', methods = ["GET","POST"])
@app.route('/request/<path:url>', methods = ["GET","POST"])
def screenAndRequest(url):
	if request.method == 'POST':

		url = urlparse(url,'http').geturl()

		if not is_empty(request.data):
			request.get_json(force=False)
		# request.data ~= {"viewport":[1024,1024],"timeout":60}
		# FIXME - Parse the data more securely and efficiently - type &| length verification
		if 'timeout' not in request.json:
			request.json['timeout'] = 60
		else:
			try:
				request.json['timeout'] = int(request.json['timeout'])
			except ValueError as e:
				return jsonify({'error': 'Bad Request, timeout: Requires valid integer'}), 400

		if 'viewport' not in request.json:
			request.json['viewport'] = [1024,1024]
		else:
			try:
				#request.json['viewport'] = ast.literal_eval(request.json['viewport'])
				if (len(ast.literal_eval(request.json['viewport'])) != 2 ):
					raise ValueError('viewport array length != 2')
			except ValueError as e:
				return jsonify({'error': 'Bad Request, viewport:  Must provide the following format [x,x]'}), 400
		
		pprint(request.json)
		
		payload = {"url": url, "viewport": request.json['viewport'], "timeout": request.json['timeout']}
		pprint(payload)
		try:
			output = requests.post(puppeteer + '/request', json = payload, timeout=request.json['timeout']).content
			return(output),200
		except requests.exceptions.ConnectionError as e:
			return jsonify({'error': 'Server Error, couldn\'t connect to Puppeteer instance'}), 500
			pass
		except requests.exceptions.ReadTimeout as e:
			return jsonify({'error': 'Server timeout, couldn\'t get a response from Puppeteer instance in '+str(request.json['timeout'])+' seconds.'}), 500
			pass
		return(output),200
	else:
		return jsonify({'error': 'Method not allowed!'}), 400

@app.errorhandler(404)
def not_found(error):
	return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
	return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)
