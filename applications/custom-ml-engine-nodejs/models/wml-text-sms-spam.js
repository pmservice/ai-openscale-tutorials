const log4js = require("log4js");
const logger = log4js.getLogger();
const rp = require("../request-wrapper");
const btoa = require("btoa");

function _getWmlToken() {
    const url = "https://us-south.ml.cloud.ibm.com/v3/identity/token"

    if (process.env.WML_USERNAME && process.env.WML_PASSWORD) {
        const token = btoa(process.env.WML_USERNAME + ":" + process.env.WML_PASSWORD)
        const opts = {
            uri: url,
            json: true,
            headers: {
                Authorization: "Basic " + token
            }
        };
        return rp.get(opts).then((result) => {
			logger.info("Got the WML Token");
			console.log(result)
            return Promise.resolve(result.token);
        }).catch((error) => {
            logger.error(error)
            return Promise.reject();
        });
    }
	
    return Promise.reject("WML Username and Password are not present in environment")
}

function score(req, res) {
	const url = "https://us-south.ml.cloud.ibm.com/v3/wml_instances/01aeb44d-765f-4e54-b3fd-5de520192698/deployments/e81600ad-de66-4150-bae2-b00590048861/online";

	_getWmlToken().then((token) => {
		const opts = {
			uri: url,
			json: true,
			headers: {
				Authorization: "Bearer " + token
			},
			body: req.body
		};
		rp.post(opts, req).then((result) => {
			logger.info(JSON.stringify(result));
			res.send(manipulate(result));
		}).catch((error) => {
			res.status(500).send(error);
		});
	}).catch((error) => {
		res.status(500).send(error);
	});
}

function manipulate(result) {
	fields = result.fields;
	fields.splice(1, 4);

	values = result.values.map((value) => {
		value.splice(1, 4);
		return value;
	})
	return {fields, values};
}

module.exports = {
	score
};