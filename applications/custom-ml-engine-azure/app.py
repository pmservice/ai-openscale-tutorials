from flask import Flask


app = Flask(__name__, static_url_path='')

import flask
import requests
import json


def convert_user_output_2_openscale(output_data):
    output_data = json.loads(output_data)
    users_records = output_data['output']
    openscale_fields = list(users_records[0])
    openscale_values = [[rec[k] for k in openscale_fields] for rec in users_records]

    return {'fields': openscale_fields, 'values': openscale_values}


def convert_openscale_input_2_user(input_data):
    openscale_fields = input_data['fields']
    openscale_values = input_data['values']
    users_records = [{k: v for k, v in zip(openscale_fields, rec)} for rec in openscale_values]

    return {'input': users_records}


@app.route("/v1/deployments/credit/online", methods=["POST"])
def credit_online():

    # original scoring endpoint with credit risk deployment (Azure ML Service)
    scoring_endpoint = 'http://20.189.138.213:80/score'
    scoring_headers = {'Content-Type': 'application/json'}
    openscale_output = None

    if flask.request.method == "POST":
        payload = flask.request.get_json()

        if payload is not None:
            user_input = convert_openscale_input_2_user(payload)
            response = requests.post(scoring_endpoint, json=user_input, headers=scoring_headers)
            openscale_output = convert_user_output_2_openscale(response.json())

    return flask.jsonify(openscale_output)


@app.route("/v1/deployments", methods=["GET"])
def get_deployments():
    response = {}

    if flask.request.method == "GET":
        host_url = flask.request.host
        response = {
            "count": 1,
            "resources": [
                {
                    "metadata": {
                        "guid": "credit",
                        "created_at": "2019-01-01T10:11:12Z",
                        "modified_at": "2019-01-02T12:00:22Z"
                    },
                    "entity": {
                        "name": "German credit risk perturbed scoring endpoint",
                        "description": "Scikit-learn credit risk model deployment",
                        "scoring_url": "https://{}/v1/deployments/credit/online".format(host_url),
                        "asset": {
                              "name": "credit",
                              "guid": "credit"
                        },
                        "asset_properties": {
                               "problem_type": "binary",
                               "input_data_type": "structured",
                        }
                    }
                }
            ]
        }

    return flask.jsonify(response)
