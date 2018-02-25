# main_with_json.py
import json

with open('marvin.json', 'r') as f:
    config = json.load(f)

#secret_key = config['DEFAULT']['SECRET_KEY'] # 'secret-key-of-myapp'
#ci_hook_url = config['CI']['HOOK_URL'] # 'web-hooking-url-from-ci-service'

def allValues():
	return json.dumps(config, indent=4)

def infoValues():
	return json.dumps(config["INFO"], indent=4)

def limitValue():
	return(config["INFO"]["limits"]["parallel_tasks"])

def pingValues(key):
	return(config["INFO"]["ping"][key])

def puppeteerValues(key):
	return(config["Puppeteer"][key])