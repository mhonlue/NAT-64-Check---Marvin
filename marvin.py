#!flask/bin/python
from flask import Flask, json, jsonify, make_response, request, abort
from pprint import pprint
import subprocess, socket

app = Flask(__name__)

def runPing(cmdArray):
	process = subprocess.Popen(cmdArray, stdout=subprocess.PIPE)
	# Run the command
	output = process.communicate()[0]
	return output

@app.route('/')
def root():
  return('Welcome')

@app.route('/info')
def getInfo():
	response = {
				  "type": "Chrome Marvin",
				  "version": "1.0.0",
				  "browser": {
				    "name": "Chromium",
				    "version": "62.0.3170.2"
				  },
				  "instance_type": "nat64",
				  "name": "sjms-42",
				  "network": {
				    "ipv4": {
				      "address": "192.168.0.42/24",
				      "gateway": "192.168.0.1"
				    },
				    "ipv6": {
				      "address": "2001:db8::42/64",
				      "gateway": "2001:db8::1"
				    },
				    "dns_server": "2001:db8::53"
				  },
				  "limits": {
				    "parallel_tasks": 15
				  }
				}
	return jsonify(response), 200

@app.route('/ping/', methods = ["GET","POST"])
@app.route('/ping/<hostname>', methods = ["GET","POST"])
def ping(hostname):
	if request.method == 'POST':
		request.get_json(force=True);
		# request.data ~= {"size":"56","count":"5","pmtu":"want","timeout":"60"}
		dataBytes = request.data
		data = json.loads(dataBytes) #Convert from bytes format to JSON

		cmd = '-c%s -n -s%s -M%s'% (data['count'] , data['size'] , data['pmtu'])
		output = runPing(['ping', cmd , hostname])

		pprint('ping %s %s' %(cmd, hostname))
		return(output),200
	else:
		return('Method not allowed!'), 400

@app.route('/ping6/', methods = ["GET","POST"])
@app.route('/ping6/<hostname>', methods = ["GET","POST"])
def ping6(hostname):
	if request.method == 'POST':
		request.get_json(force=True);
		# request.data ~= {"size":"56","count":"5","pmtu":"want","timeout":"60"}
		dataBytes = request.data
		data = json.loads(dataBytes) #Convert from bytes format to JSON

		cmd = '-c%s -n -s%s -M%s'% (data['count'] , data['size'] , data['pmtu'])
		output = runPing(['ping6', cmd , hostname])

		pprint('ping6 %s %s' %(cmd, hostname))
		return(output),200
	else:
		return('Method not allowed!'), 400

if __name__ == '__main__':
    app.run(debug=True)
