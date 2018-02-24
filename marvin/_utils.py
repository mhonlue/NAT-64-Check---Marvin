from flask import request
from marvin_config import *
import json
import subprocess, socket

def runPing(cmdArray):
        process = subprocess.Popen(cmdArray, stdout=subprocess.PIPE)
        # Run the command
        output = process.communicate()[0].decode("utf-8") 
        return output

def is_empty(any_structure):
        if any_structure:
                return False
        else:
                return True

def punyHostname(hostname):
#       str = hostname.encode().decode('utf-8')
#       out = str.encode('punycode')
#       return out.decode()
#       url_parts = urlparse(hostname, scheme='http')
#       return url_parts.netloc.encode('idna').decode('utf-8')
        return hostname

def ping_options():
	request.get_json(force=True);
	dataBytes = request.data.decode('utf-8')
	data = json.loads(dataBytes) #Convert from bytes format to JSON
	if 'count' not in data:
	        data['count'] = pingValues("count")
	if 'size' not in data:
	        data['size'] = pingValues("size")
	if 'pmtu' not in data:
	        data['pmtu'] = pingValues("pmtu")

	return data