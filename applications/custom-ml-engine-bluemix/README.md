# Custom machine learning engine
## Serving Azure and Scikit-learn models on IBM Cloud (bluemix)

The repository contains the code for creating custom deployment of Scikit-learn (Credit Risk) on IBM Cloud.
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
   $ cd applications/custom-ml-engine-bluemix
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
DEPLOYMENTS_URL = 'http://169.xx.xxx.xxx:30080/v1/deployments'
header = {'Content-Type':'application/json'}
r = requests.get(DEPLOYMENTS_URL, headers=header)

print(str(r.text))
```
Response:
```json
{'count': 2, 'resources': [{'metadata': {'guid': 'credit', 'modified_at': '2019-01-02T12:00:22Z', 'created_at': '2019-01-01T10:11:12Z'}, 'entity': {'description': 'Scikit-learn credit risk model deployment', 'asset': {'name': 'credit', 'guid': 'credit'}, 'scoring_url': 'https://custom-engine.azurewebsites.net/v1/deployments/credit/online', 'name': 'German credit risk compliant deployment', 'asset_properties': {'input_data_type': 'structured', 'problem_type': 'binary'}}}, {'metadata': {'guid': 'circle', 'modified_at': '2019-01-02T12:00:22Z', 'created_at': '2019-01-01T10:11:12Z'}, 'entity': {'description': 'Azure ML service circle surface prediction deployment', 'asset': {'name': 'circle', 'guid': 'circle'}, 'scoring_url': 'https://custom-engine.azurewebsites.net/v1/deployments/circle/online', 'name': 'Circle model deployment', 'asset_properties': {'input_data_type': 'structured', 'problem_type': 'regression'}}}]}
```

### Score

Request:
```python
SCORING_URL = "http://169.xx.xxx.xxx:30080/v1/deployments/circle/online"

payload = {'values': [[10], [20]], 'fields': ['radius']}
header = {'Content-Type':'application/json'}

r = requests.post(SCORING_URL, json=payload, headers=header)

print(str(r.text))
```
Response:
```json
{'values': [[314.3231432314323], [1257.2925729257292]], 'fields': ['area']}
```


## References:
1. [The Keras Blog, "Building a simple Keras + deep learning REST API"](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)
2. [AI OpenScale service](https://console.bluemix.net/catalog/services/ai-openscale)
3. [REST API specification](https://aiopenscale-custom-deployement-spec.mybluemix.net/)
4. [Sample notebook:  Custom deployment scoring examples](TBD)
5. [Sample notebook: Data Mart configuration for custom deployment](TBD)

