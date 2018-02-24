const Puppeteer = require('puppeteer');
const express = require('express');

const app = express();
const port = 3001;

app.use(express.json());

const puppeteer = Puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--incognito']
})

process.on('exit', function(){
	puppeteer.close(); // Ensure that the browser process is stopped properly
})

async function getData(url, viewport, pageTimeout){
	const browser = await puppeteer
	const page = await browser.newPage();
	const resources = [];
	const consoleArray = [];
	
	// Event - Push any console messages to consoleArray
	page.on('console', msg => {
		consoleArray.push( msg.text );
	});
	// page.on('request', msg =>{
	// 	console.log(msg); // Possible the key to line 38 - date/time of the request
	// });

	page.on('response', response => {
		// response.headers.date = new Date('response.headers.date').toISOString(); // FIXME - convert all date/time to round-trip date/time variant
		resourceObject = { // Create Object for current resource
			"success": response.ok,
			"request":
			{
				"method": response._request['method'],
				"url": response._request['url'],
				"headers": response._request['headers'], //FIXME - Remove the date key/value from the 'headers' object
				"time": response['headers']['date'] //FIXME - The date/time of the request doesn't look available from the API, currently using the same as the response
			},
			"response":{
				"status": response['status'],
				"headers": response['headers'],
				"time": response['headers']['date']
			}
		};
		if (!response.url.startsWith("data:") && !response.url.startsWith("blank:")){ // Because apparently data/blank protocols are tagged as separate requests on Chrome
			resources.push(resourceObject);
		}
	});
	await page.setViewport({width: viewport.width, height: viewport.height});
	await page.goto(url);
	const screenshot = Buffer.from(await page.screenshot({type: 'png', omitBackground: false })).toString('base64'); // FUTURE - Add the ability of selecting another mimetype from the POST data

	page.close()
	return {
		'request': {
			'url': url,
			'viewport': [viewport.width, viewport.height],
			'timeout': pageTimeout
		},
		'console': consoleArray,
		'image': screenshot,
		'resources': resources
	}
}

app.post('/request', function (req, res) {
	try{ // FIXME - Currently breaks when the required data (url,timeout,viewport) is not passed through POST
		let parsedViewport = JSON.parse(req.body.viewport);

		let url = req.body.url;
		let pageTimeout = req.body.timeout;
		let viewport = { width: parsedViewport[0], height: parsedViewport[1] };
		console.log(req.body);

		getData(url, viewport, pageTimeout).then(function(data) {
	        res.send(data);
	    });
	}
	catch(err){
		console.log(err);
	}
	
})

app.listen(port, () => console.log('Puppeteer listening on port',port,'!'));
