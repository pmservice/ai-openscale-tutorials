# Custom machine learning engine
## Serving Keras, Spark and Scikit-learn models

The repository contains the code for creating custom deployment of Keras ResNet50 model (images classification) and Scikit-learn (Credit Risk) on IBM Cloud.
Custom deployment provides REST API endpoints to score the model (predict image class) and to list deployment endpoints.

**Note**: To be able to integrate custom deployment with [Watson OpenScale](https://console.bluemix.net/catalog/services/ai-openscale) features it must follow [REST API specification](https://aiopenscale-custom-deployement-spec.mybluemix.net/).


## Requirements

- python 3.5 or 3.6
- pip
- python libs: cfenv, Flask, watson-developer-cloud, gevent, requests, tensorflow, keras, ibmcloudenv, livereload, pillow, numpy, scikit-learn, xgboost

User also should have account on Bluemix (IBM Cloud) with active us-south region. 


## Deployment

### Initial configuration

Clone repository and enter cloned project directory:

   ```bash
   $ git clone https://github.com/pmservice/ai-openscale-tutorials
   $ cd applications/custom-ml-engine
   ```

### Deployment and run on local environment

Run:

```bash
$ pip install -r requirements.txt
$ export PYTHON_FLASK=app.py
$ python -m flask run
```

Application server will be available at `127.0.0.1:5000`.


### Deployment and run on IBM Cloud (Bluemix)

Update manifest.yml file and provide `<APP_NAME>` and `<APP_ROUTE>`, for example:
```
name: PythonWebAppwithFlask
route: python-web-app-with-flask.mybluemix.net
```

Save the manifest file and run the following commands to publish app as a cloud foundry app on Bluemix.
```
bx api api.ng.bluemix.net
bx login
bx app push
```
   
    
## Submitting REST API requests

### List deployments
Request:
```python
KERAS_REST_API_URL = 'http://169.xx.xxx.xxx:30080/v1/deployments'
header = {'Content-Type':'application/json'}
r = requests.get(KERAS_REST_API_URL, headers=header)

print(str(r.text))
```
Response:
```json
{"count":2,"resources":[{"entity":{"deployable_asset":{"created_at":"2016-12-01T10:11:12Z","guid":"569ac899-c0d1-4892-b09f-7415e7eb7948","name":"my ResNet50 model","type":"model","url":"http://github.com/models/my_model.h5"},"description":"description","model_type":"tf-1.5","name":"ResNet50 aios compliant deployment","runtime_environment":"py-3.5","scoring_url":"https://keras-resnet50.mybluemix.net/v1/deployments/aios_compliant/online","status":"ACTIVE","status_message":"string","type":"online"},"metadata":{"created_at":"2016-12-01T10:11:12Z","guid":"string","modified_at":"2016-12-02T12:00:22Z","url":"string"}},{"entity":{"deployable_asset":{"created_at":"2016-12-01T10:11:12Z","guid":"569ac899-c0d1-4892-b09f-7415e7eb79xx","name":"my ResNet50 model","type":"model","url":"http://github.com/models/my_model.h5"},"description":"description","model_type":"tf-1.5","name":"ResNet50 custom deployment","runtime_environment":"py-3.5","scoring_url":"https://keras-resnet50.mybluemix.net/v1/deployments/custom/online","status":"ACTIVE","status_message":"string","type":"online"},"metadata":{"created_at":"2016-12-01T10:11:12Z","guid":"string","modified_at":"2016-12-02T12:00:22Z","url":"string"}}]}
```

### Score

Request:
```python
def prepare_payload(image_path):
    image = Image.open(image_path)

    if image.mode is not "RGB":
        image = image.convert("RGB")

    image = image.resize((224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)
    image_list = image.tolist()

    return {'values': image_list}
```
```python
KERAS_REST_API_URL = "http://169.xx.xxx.xxx:30080/v1/deployments/compliant/online"

payload = prepare_payload('labrador.jpg')
header = {'Content-Type':'application/json'}

r = requests.post(KERAS_REST_API_URL, json=payload, headers=header)

print(str(r.text))
```
Response:
```json
{"fields":["probabilities","prediction","prediction_probability"],"labels":["Labrador_retriever","Chesapeake_Bay_retriever","Rottweiler","curly-coated_retriever","Rhodesian_ridgeback"],"values":[[["0.70551187","0.22909379","0.030718252","0.0062348368","0.0053016352"],"Labrador_retriever","0.70551187"]]}
```


## References:
1. [The Keras Blog, "Building a simple Keras + deep learning REST API"](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)
2. [AI OpenScale service](https://console.bluemix.net/catalog/services/ai-openscale)
3. [REST API specification](https://aiopenscale-custom-deployement-spec.mybluemix.net/)
4. [Sample notebook:  Custom deployment scoring examples](TBD)
5. [Sample notebook: Data Mart configuration for custom deployment](TBD)

