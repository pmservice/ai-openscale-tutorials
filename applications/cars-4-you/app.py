import os
from flask import Flask, send_from_directory, request, jsonify, logging, render_template
from wml import WML
from utils import get_wml_vcap

app = Flask(__name__)

wml_client = WML(get_wml_vcap())


@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/deployments', methods=['GET'])
def deployments():

    try:
        response = wml_client.get_cars4u_deployments()
        return jsonify(response), 200
    except Exception as e:
        return str(e), 500


@app.route('/score', methods=['POST'])
def score():
    payload = request.get_json(force=True)
    app.logger.debug("Scoring request: {}".format(payload))
    try:
        response = wml_client.get_recommendation(payload)
        return jsonify(response), 200
    except Exception as e:
        return str(e), 500

# @app.route('/analyze/area', methods=['POST'])
# def analyze_area():
#     payload = request.get_json(force=True)
#     app.logger.debug("Area request: {}".format(payload))
#     try:
#         response = wml_client.analyze_business_area(payload)
#         return jsonify(response), 200
#     except Exception as e:
#         return str(e), 500
#
#
# @app.route('/analyze/satisfaction', methods=['POST'])
# def analyze_satisfaction():
#     comment = request.get_data().decode('utf-8')
#     app.logger.debug("Comment to analyze: {}".format(comment))
#     try:
#         satisfaction = wml_client.analyze_satisfaction(comment)
#         app.logger.debug("Predicted satisfaction: {}".format(satisfaction))
#         return satisfaction
#     except Exception as e:
#         return str(e), 500
#
#
# @app.route('/functions/satisfaction', methods=['GET'])
# def functions_satisfaction():
#     deployment_array = wml_client.get_function_deployments(keyword="satisfaction")
#     app.logger.debug("Satisfaction functions: {}".format(deployment_array))
#     response = {
#         "deployments" : deployment_array
#     }
#     return jsonify(response)
#
#
# @app.route('/functions/area', methods=['GET'])
# def functions_area():
#     deployment_array = wml_client.get_function_deployments(keyword="area")
#     app.logger.debug("Area functions: {}".format(deployment_array))
#     response = {
#         "deployments" : deployment_array
#     }
#     return jsonify(response)
#
#
# @app.route('/functions', methods=['POST'])
# def functions():
#     models = request.get_json(force=True)
#     app.logger.info("Request to anayze: ")
#     app.logger.info(models)
#     try:
#         wml_client.update_scoring_functions(deployments=models)
#         return jsonify("ok"), 200
#     except Exception as e:
#         app.logger.info(str(e))
#         return jsonify(str(e)), 500


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=int(port))
