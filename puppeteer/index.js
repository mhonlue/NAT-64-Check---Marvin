const Puppeteer = require('puppeteer');
const express = require('express');

const app = express();
const port = 3001;

const puppeteer = Puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox']
})

process.on('exit', function(){
	puppeteer.close(); // Ensure that the browser process is stopped properly
})

async function getData(url, viewport){
	const browser = await puppeteer
	const page = await browser.newPage();
	const requests = [];
	page.on('response', response => {
		responseObject = {url: response.url, status: response.status, type: response.headers['content-type']};
		if (!response.url.startsWith("data:")){ // Because apparently data tags are marked as separate requests on Chrome
			requests.push(responseObject);
		}
	});
	//page.setViewport({width: 1920 ,height: 1080});
	await page.goto(url);
	const screenshot = Buffer.from(await page.screenshot({type: 'png', omitBackground: false })).toString('base64');

	page.close()
	return {
		requests: requests,
		screenshot: screenshot
	}
}

app.get('/request', function (req, res) {
	console.log('Request URL:', req.originalUrl)
	getData('http://google.com',{width: 640 ,height: 480}).then(function(data) {
        res.send(data);
    });
})

app.listen(port, () => console.log('Puppeteer listening on port',port,'!'));
