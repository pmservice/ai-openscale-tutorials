const log4js = require("log4js");
const logger = log4js.getLogger();
const aws = require("aws4")
const rp = require("../request-wrapper");

function score(req, res) {
    const opts = aws.sign({
        hostname: "https://runtime.sagemaker.us-east-2.amazonaws.com",
        path: "/endpoints/arsuryan-iris-mc-endpoint-2018-11-29-05-37-34/invocations",
        body: JSON.stringify(createPayload(req)),
        headers: {
            "Content-Type": "application/json"
        }
    })
    opts["url"] = opts["hostname"] + opts["path"]
    delete opts["hostname"]
    delete opts["path"]
    opts["rejectUnauthorized"] = false
    rp.post(opts, req).then((result) => {
		logger.info(result);
		const manipulated = manipulate(req.body.values, JSON.parse(result).predictions)
        const fields = req.body.fields;
        fields.push("prediction", "probability")
		res.send({fields, values: manipulated});
	}).catch((error) => {
		res.status(500).send(error);
	});
}

function manipulate(input_values, output_values) {
    i = 0;
    values = []
    for (i=0; i< input_values.length; i++)  {
        values.push([...input_values[i], output_values[i].predicted_label, output_values[i].score])
    }
	return values;
}

function createPayload(req) {
	logger.info(JSON.stringify(req.body));
	const scoringInputs = req.body.values.map((value) => ({ features: value }));
	return {instances: scoringInputs};
}

module.exports = {
	score
};
