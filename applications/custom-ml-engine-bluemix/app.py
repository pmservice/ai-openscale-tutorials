import os
from flask import Flask

app = Flask(__name__, static_url_path='')

if 'FLASK_LIVE_RELOAD' in os.environ and os.environ['FLASK_LIVE_RELOAD'] == 'true':
    import livereload

    app.debug = True
    server = livereload.Server(app.wsgi_app)
    server.serve(port=os.environ['port'], host=os.environ['host'])

import pandas as pd
import flask
import os
from sklearn.externals import joblib
import requests
import json

credit_model = None


def load_credit_model():
    global credit_model

    credit_model_path = os.path.join(os.getcwd(), 'models', 'credit', 'german_credit_risk.joblib')
    credit_model = joblib.load(credit_model_path)


load_credit_model()


@app.route("/v1/deployments/credit/online", methods=["POST"])
def credit_online():
    response = {}
    labels = ['Risk', 'No Risk']

    if flask.request.method == "POST":
        payload = flask.request.get_json()

        if payload is not None:
            df = pd.DataFrame.from_records(payload['values'], columns=payload['fields'])
            scores = credit_model['model'].predict_proba(df).tolist()
            predictions = credit_model['postprocessing'](credit_model['model'].predict(df))
            response = {'fields': ['prediction', 'probability'], 'labels': labels,
                        'values': list(map(list, list(zip(predictions, scores))))}

    return flask.jsonify(response)


@app.route("/v1/deployments/circle/online", methods=["POST"])
def circle_online():
    response = {}
    scoring_url = 'http://52.180.94.47:80/score'
    prediction_field = 'area'
    predictions = []

    if flask.request.method == "POST":
        payload = flask.request.get_json()

        if payload is not None:
            values = payload['values']
            fields = payload['fields']

            for value in values:
                result = json.loads(requests.post(scoring_url, json={fields[0]: value[0]}).json())
                predictions.append([result[prediction_field]])

            response = {'fields': [prediction_field], 'values': predictions}

    return flask.jsonify(response)


@app.route("/v1/deployments", methods=["GET"])
def get_deployments():
    response = {}

    if flask.request.method == "GET":
        host_url = flask.request.host
        response = {
            "count": 2,
            "resources": [
                {
                    "metadata": {
                        "guid": "credit",
                        "created_at": "2019-01-01T10:11:12Z",
                        "modified_at": "2019-01-02T12:00:22Z"
                    },
                    "entity": {
                        "name": "German credit risk compliant deployment",
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
                },
                {
                    "metadata": {
                        "guid": "circle",
                        "created_at": "2019-01-01T10:11:12Z",
                        "modified_at": "2019-01-02T12:00:22Z"
                    },
                    "entity": {
                        "name": "Circle model deployment",
                        "description": "Azure ML service circle surface prediction deployment",
                        "scoring_url": "https://{}/v1/deployments/circle/online".format(host_url),
                        "asset": {
                            "name": "circle",
                            "guid": "circle"
                        },
                        "asset_properties": {
                            "problem_type": "regression",
                            "input_data_type": "structured",
                        }
                    }
                }
            ]
        }

    return flask.jsonify(response)
