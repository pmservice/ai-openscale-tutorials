const log4js = require("log4js");
const _ = require("lodash")
const logger = log4js.getLogger();
const rp = require("../request-wrapper");

function score(req, res) {
	// const url = "https://ussouthcentral.services.azureml.net/workspaces/f11c86a33a0e48a8a4b6f13058d81aad/services/f35498a6623645068c89275adf7afc1c/execute?api-version=2.0&details=true";
	const url = "https://ussouthcentral.services.azureml.net/workspaces/f11c86a33a0e48a8a4b6f13058d81aad/services/658329021c5e4dfda84920b74087391b/execute?api-version=2.0&details=true";
	const apikey = process.env.AZURE_APIKEY;
	const opts = {
		uri: url,
		json: true,
		headers: {
			Authorization: "Bearer " + apikey,
			"Content-Type": "application/json",
			Accept: "application/json"
		},
		body: createPayload(req)
	};
	rp.post(opts, req).then((result) => {
		logger.info(JSON.stringify(result));
		res.send(manipulate(result));
	}).catch((error) => {
		res.status(500).send(error);
	});
}

function manipulate(result) {
	fields = result.Results.output1.value.ColumnNames;
	fields.splice(4, 7, "probability");

	values = result.Results.output1.value.Values.map((value) => {
		probabilities = value.slice(5,-1);
		probabilities = probabilities.map(probability => parseFloat(probability));
		// prediction = _.indexOf(probabilities, _.max(probabilities))
		value.splice(4, 7, probabilities);
		return value;
	})
	return {fields, values};
}

function createPayload(req) {
	logger.info(JSON.stringify(req.body));
	payload = {
		Inputs: {
			input1: {
				ColumnNames: req.body.fields,
				Values: req.body.values
			}
		}
	}
	logger.info(JSON.stringify(payload))
	return payload;
}

module.exports = {
	score
};