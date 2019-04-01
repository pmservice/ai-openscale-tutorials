import os
from flask import Flask


app = Flask(__name__, static_url_path='')


if 'FLASK_LIVE_RELOAD' in os.environ and os.environ['FLASK_LIVE_RELOAD'] == 'true':
	import livereload
	app.debug = True
	server = livereload.Server(app.wsgi_app)
	server.serve(port=os.environ['port'], host=os.environ['host'])


from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from keras.applications import ResNet50
from keras import backend
import pandas as pd
import numpy as np
import flask
import os
from sklearn.externals import joblib
import requests
import json


resnet50_model = None
action_model = None
credit_model = None
boston_model = None


def load_resnet50_model():
    global resnet50_model

    with backend.get_session().graph.as_default() as g:
        resnet50_model = ResNet50(weights="imagenet")


def load_credit_model():
    global credit_model

    credit_model_path = os.path.join(os.getcwd(), 'models', 'credit', 'german_credit_risk.joblib')
    credit_model = joblib.load(credit_model_path)


def preprocess_image(image, target_shape=None):
    if type(image) is list:
        image = np.array(image)
    elif target_shape is not None:
        if image.mode is not "RGB":
            image = image.convert("RGB")

        image = image.resize(target_shape)
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = imagenet_utils.preprocess_input(image)

    return image


load_resnet50_model()
load_credit_model()


@app.route("/v1/deployments/resnet50/online", methods=["POST"])
def resnet50_online():
    response = {}
    images = []
    fields = ['probabilities', 'prediction', 'prediction_probability']
    prediction_values = []

    if flask.request.method == "POST":
        payload = flask.request.get_json()

        if payload is not None:
            images_list = payload['values']

            for image in images_list:
                images.append(preprocess_image(image))

            with backend.get_session().graph.as_default() as g:
                scores = resnet50_model.predict(np.concatenate(images, axis=0))

            results = imagenet_utils.decode_predictions(scores)

            for result in results:
                labels = []
                probabilities = []
                prediction_probability = 0.0
                prediction = None

                for (imagenetID, label, probability) in result:
                    probability = float(probability)
                    if probability > prediction_probability:
                        prediction_probability = probability
                        prediction = label
                    labels.append(label)
                    probabilities.append(probability)

                prediction_values.append([probabilities, prediction, prediction_probability])

            if len(images_list) == 1:
                response = {'fields': fields, 'labels': labels, 'values': prediction_values}
            else:
                response = {'fields': fields, 'values': prediction_values}

    return flask.jsonify(response)


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
            "count": 4,
            "resources": [
                {
                    "metadata": {
                        "guid": "resnet50",
                        "created_at": "2016-12-01T10:11:12Z",
                        "modified_at": "2016-12-02T12:00:22Z"
                    },
                    "entity": {
                        "name": "ResNet50 AIOS compliant deployment",
                        "description": "Keras ResNet50 model deployment for image classification",
                        "scoring_url": "https://{}/v1/deployments/resnet50/online".format(host_url),
                        "asset": {
                              "name": "resnet50",
                              "guid": "resnet50"
                        },
                        "asset_properties": {
                               "problem_type": "multiclass",
                               "input_data_type": "unstructured_image",
                        }
                    }
                },
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