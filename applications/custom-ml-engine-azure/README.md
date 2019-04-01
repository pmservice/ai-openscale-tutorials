# Custom machine learning engine
## Serving Microsoft Azure Service deployment and scikit-learn model

The repository contains the code for creating custom deployment of Azure sample circle model (regression) and scikit-learn (Credit Risk) on Azure Cloud.
Custom deployment provides REST API endpoints to score the model and to list deployment endpoints.

**Note**: To be able to integrate custom deployment with [Watson OpenScale](https://console.bluemix.net/catalog/services/ai-openscale) features it must follow [REST API specification](https://aiopenscale-custom-deployement-spec.mybluemix.net/).


## Requirements

- python 3.5 or 3.6
- pip
- python libs: cfenv, Flask, watson-developer-cloud, gevent, requests, tensorflow, keras, ibmcloudenv, livereload, pillow, numpy, scikit-learn

User also should have account on Azure Portal. 


## Deployment

### Initial configuration

Clone repository and enter cloned project directory:

   ```bash
   $ git clone https://github.com/pmservice/ai-openscale-tutorials
   $ cd ai-openscale-tutorials/applications/custom-ml-engine-azure
   ```

### Deployment and run on local environment

Run:

```bash
$ pip install -r requirements.txt
$ export PYTHON_FLASK=app.py
$ python -m flask run
```

Application server will be available at `127.0.0.1:5000`.


### Deployment and run on Azure Cloud (App Services)

#### Login to Azure Portal and open bash console
#### Using console clone git project, enter project directory and deploy app:
```bash
$ git clone https://github.com/pmservice/ai-openscale-tutorials.git
$ cd ai-openscale-tutorials/applications/custom-ml-engine-azure
$ az webapp up -n <your app name>
```
    
## Submitting REST API requests

### List deployments
Request:
```python
APP_URL = <put your app hostname>
DEPOYMENTS_URL = APP_URL + '/v1/deployments'
r = requests.get(DEPOYMENTS_URL)

print(str(r.text))
```
Response:
```json
{'count': 2, 'resources': [{'metadata': {'guid': 'credit', 'modified_at': '2019-01-02T12:00:22Z', 'created_at': '2019-01-01T10:11:12Z'}, 'entity': {'description': 'Scikit-learn credit risk model deployment', 'asset': {'name': 'credit', 'guid': 'credit'}, 'scoring_url': 'https://custom-engine.azurewebsites.net/v1/deployments/credit/online', 'name': 'German credit risk compliant deployment', 'asset_properties': {'input_data_type': 'structured', 'problem_type': 'binary'}}}, {'metadata': {'guid': 'circle', 'modified_at': '2019-01-02T12:00:22Z', 'created_at': '2019-01-01T10:11:12Z'}, 'entity': {'description': 'Azure ML service circle surface prediction deployment', 'asset': {'name': 'circle', 'guid': 'circle'}, 'scoring_url': 'https://custom-engine.azurewebsites.net/v1/deployments/circle/online', 'name': 'Circle model deployment', 'asset_properties': {'input_data_type': 'structured', 'problem_type': 'regression'}}}]}
```

### Score
Request:
```python
APP_URL = <put your app hostname>
SCORING_URL = APP_URL + '/v1/deployments/circle/online'
payload={'fields':['radius'], 'values':[[10],[20]]}

r = requests.post(SCORING_URL, json=payload)

print(str(r.json()))
```
Response:
```json
{'values': [[314.3231432314323], [1257.2925729257292]], 'fields': ['area']}
```


## References:
1. [The Keras Blog, "Building a simple Keras + deep learning REST API"](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)
2. [AI OpenScale service](https://console.bluemix.net/catalog/services/ai-openscale)
3. [REST API specification](https://aiopenscale-custom-deployement-spec.mybluemix.net/)

