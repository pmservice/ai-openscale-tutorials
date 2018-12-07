from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from keras.applications import ResNet50
from pyspark.ml import PipelineModel
from keras import backend
import pandas as pd
from PIL import Image
import numpy as np
import flask
import io
import os
from pyspark.sql.session import SparkSession


PUBLIC_IP = "173.193.75.3"
NODE_PORT = "31520"

app = flask.Flask(__name__)
resnet50_model = None
action_model = None
spark = SparkSession.builder.getOrCreate()
application_url = "http://{}:{}".format(PUBLIC_IP, NODE_PORT)


def load_resnet50_model():
    global resnet50_model

    with backend.get_session().graph.as_default() as g:
            resnet50_model = ResNet50(weights="imagenet")


def load_action_model():
    global action_model
    global spark

    action_model_path = os.path.join(os.getcwd(), 'models', 'action')
    action_model = PipelineModel.load(action_model_path)


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


def convert_vector(value):
    from pyspark.ml.linalg import SparseVector, DenseVector
    if type(value) is SparseVector:
        return [float(value.size), [float(el) for el in list(value.indices)], [float(el) for el in list(value.values)]]
    if type(value) is DenseVector:
        return [float(el) for el in value.values]
    return value


def convert_values(array):
    values = []

    for a in array:
        values.append([convert_vector(item) for item in a])

    return values


@app.route("/v1/deployments/resnet50_non_compliant/online", methods=["POST"])
def non_compliant_resnet50_online():
    response = {}
    predictions = []

    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            image = preprocess_image(image, target_shape=(224, 224))

            with backend.get_session().graph.as_default() as g:
                scores = resnet50_model.predict(image)
            results = imagenet_utils.decode_predictions(scores)

            for (imagenetID, label, prob) in results[0]:
                predictions.append({'prediction': label, 'probability': str(prob)})

            response = {"Results:": predictions}

    return flask.jsonify(response)


@app.route("/v1/deployments/resnet50/online", methods=["POST"])
def resnet50_online():
    response = {}
    fields = ['probabilities', 'prediction', 'prediction_probability']
    labels = []
    probabilities = []
    prediction_probability = 0.0
    prediction = None

    if flask.request.method == "POST":
        payload = flask.request.get_json()

        if payload is not None:
            image_list = payload['values']
            image = preprocess_image(image_list)

            with backend.get_session().graph.as_default() as g:
                scores = resnet50_model.predict(image)

            results = imagenet_utils.decode_predictions(scores)

            for (imagenetID, label, probability) in results[0]:
                probability = float(probability)
                if probability > prediction_probability:
                    prediction_probability = probability
                    prediction = label
                labels.append(label)
                probabilities.append(probability)

            response = {'fields': fields, 'labels': labels,
                        'values': [[probabilities, prediction, prediction_probability]]}

    return flask.jsonify(response)


@app.route("/v1/deployments/action/online", methods=["POST"])
def action_online():
    global spark
    response = {}
    labels = ['NA', 'Free Upgrade', 'On-demand pickup location', 'Voucher', 'Premium features']

    if flask.request.method == "POST":
        payload = flask.request.get_json()

        if payload is not None:
            df = spark.createDataFrame(payload['values'], payload['fields'])
            scores = action_model.transform(df)
            pd_scores = scores.toPandas()
            response = {'fields': scores.columns, 'labels': labels, 'values': convert_values(pd_scores.values.tolist())}

    return flask.jsonify(response)


@app.route("/v1/deployments", methods=["GET"])
def get_deployments():
    response = {}

    if flask.request.method == "GET":
        response = {
            "count": 3,
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
                        "scoring_url": "{}/v1/deployments/resnet50/online".format(application_url),
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
                        "guid": "resnet50_non_compliant",
                        "created_at": "2016-12-01T10:11:12Z",
                        "modified_at": "2016-12-02T12:00:22Z"
                    },
                    "entity": {
                        "name": "ResNet50 AIOS non compliant deployment",
                        "description": "Keras ResNet50 model deployment for image classification",
                        "scoring_url": "{}/v1/deployments/resnet50_non_compliant/online".format(application_url),
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
                        "guid": "action",
                        "created_at": "2016-12-01T10:11:12Z",
                        "modified_at": "2016-12-02T12:00:22Z"
                    },
                    "entity": {
                        "name": "action deployment",
                        "description": "area and action spark models deployment",
                        "scoring_url": "{}/v1/deployments/action/online".format(application_url),
                        "asset": {
                            "name": "area and action prediction",
                            "guid": "action"
                        },
                        "asset_properties": {
                            "problem_type": "multiclass",
                            "input_data_type": "structured",
                        }
                    }
                }

            ]
        }

    return flask.jsonify(response)


if __name__ == "__main__":
    load_resnet50_model()
    load_action_model()
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port))
