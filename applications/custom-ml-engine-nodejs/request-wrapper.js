const request = require("request");
const moduleLogger = require("log4js").getLogger("request-wrapper");

var requestPromise = function(options, req, acceptedStatusCodes, logger) {
	const codes = acceptedStatusCodes || [200];
	if (!options.headers) {
		options.headers = {};
	}
	const start = Date.now();
	return new Promise((resolve, reject) => {
		request(options, (err, res, body) => {
			if (logger) {
				logger.info((options.method || "GET") + " " + (options.url || options.uri) + ": " + (res ? res.statusCode : "no response"));
			}
			const time = Date.now() - start;
			if (time > 1000) {
				// log any slow responses
				moduleLogger.warn(`Slow response (${time}ms) from ${options.method || "GET"} ${options.url || options.uri}`);
			}
			if (err) {
				if (logger) {
					logger.error(err);
				}
				if (res) {
					err.statusCode = res.statusCode;
				}
				reject(err);
			} else if (codes.indexOf(res.statusCode) === -1) {
				try {
					if (body.code && body.message) {
						body = {
							errors: [body]
						};
					}
				} catch(e) {
					// ignore
				}
				const err2 = {
					error: `Unexpected status code ${res.statusCode} from API ${options.url || options.uri}`,
					details: body || "",
					statusCode: res.statusCode
				};
				if (logger) {
					logger.error(err2);
				}
				reject(err2);
			} else {
				let resObj = body;
				if (options.resolveWithFullResponse) {
					if (res && !res.body) {
						res.body = body;
					}
					resObj = res;
				}
				resolve(resObj);
			}
		});
	});
};

requestPromise.get = function(opts, req, acceptedStatusCodes, logger) {
	return requestPromise(Object.assign({}, opts, {
		method: "GET"
	}), req, acceptedStatusCodes, logger);
};

requestPromise.put = function(opts, req, acceptedStatusCodes, logger) {
	return requestPromise(Object.assign({}, opts, {
		method: "PUT"
	}), req, acceptedStatusCodes, logger);
};

requestPromise.post = function(opts, req, acceptedStatusCodes, logger) {
	return requestPromise(Object.assign({}, opts, {
		method: "POST"
	}), req, acceptedStatusCodes, logger);
};

requestPromise.delete = function(opts, req, acceptedStatusCodes, logger) {
	return requestPromise(Object.assign({}, opts, {
		method: "delete"
	}), req, acceptedStatusCodes, logger);
};

requestPromise.patch = function(opts, req) {
	return requestPromise(Object.assign({}, opts, {
		method: "patch"
	}), req);
};

module.exports = requestPromise;