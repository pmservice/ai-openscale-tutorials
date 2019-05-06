const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const log4js = require("log4js");
const logger = log4js.getLogger();
const azureProductLineWithPrediction = require("./models/azure-product-line-with-prediction");
const azureProductLine = require("./models/azure-product-line");
const azureProductLineWithOnlyProbability = require("./models/azure-product-line-with-only-probability");

const awsIris = require("./models/aws-iris")
const wmlTextSmsSpam = require("./models/wml-text-sms-spam")
const wmlImageMnist = require("./models/wml-image-mnist")
const DEPLOYMENT_LIST = require("./deployment_list.json");
const basicAuth = require('express-basic-auth')
 
app.use(bodyParser.json({limit: "12mb"}));
app.use(bodyParser.urlencoded({extended: false}));
app.use(basicAuth({
	users: { 'admin': 'password' },
	unauthorizedResponse: function(req) {
		logger.error("Not authorization.")
		return "Not authorization."
	}
}))

app.get("/v1/deployments", function (req, res) {
	res.send(DEPLOYMENT_LIST);
});

app.post("/v1/deployments/84c465e6-f87c-440f-a6ed-17fabf9454ac/online", function (req, res) {
	awsIris.score(req, res);
});

app.post("/v1/deployments/3e508dbd-0fca-4921-92f5-41fc1a8eabee/online", function (req, res) {
	req.body.fields.push("PRODUCT_LINE");
	req.body.values = req.body.values.map((value) => {
		value.push("NA");
		return value;
	});
	azureProductLineWithPrediction.score(req, res);
});

app.post("/v1/deployments/8e7b63f1-55d3-414f-a94b-c950434879c9/online", function (req, res) {
	req.body.fields.push("PRODUCT_LINE");
	req.body.values = req.body.values.map((value) => {
		value.push("NA");
		return value;
	});
	azureProductLine.score(req, res);
});

app.post("/v1/deployments/30a0b186-7931-4c96-bb3f-40d3020291d0/online", function (req, res) {
	req.body.fields.push("PRODUCT_LINE");
	req.body.values = req.body.values.map((value) => {
		value.push("NA");
		return value;
	});
	azureProductLineWithOnlyProbability.score(req, res);
});

app.post("/v1/deployments/3ba2834c-9847-4b16-a1aa-39116c406b6a/online", function (req, res) {
	wmlTextSmsSpam.score(req, res);
});

app.post("/v1/deployments/5f381f58-c188-4cc1-a0f7-f91f8f869c93/online", function (req, res) {
	wmlImageMnist.score(req, res);
});

const PORT = process.env.PORT || 5000;
var server = app.listen(PORT, function () {
	var host = server.address().address;
	var port = server.address().port;

	logger.info("Example app listening at http://%s:%s", host, port);
});