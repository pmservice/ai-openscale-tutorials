# Custom machine learning engine
## Serving Microsoft Azure Service deployment (scikit-learn model)

The repository contains the code for creating custom deployment of Azure sample circle model (regression) and scikit-learn (Credit Risk) on Azure Cloud.
Custom deployment provides REST API endpoints to score the model and to list deployment endpoints.

**Note**: To be able to integrate custom deployment with [Watson OpenScale](https://console.bluemix.net/catalog/services/ai-openscale) features it must follow [REST API specification](https://aiopenscale-custom-deployement-spec.mybluemix.net/).


## Requirements

- python 3.5 or higher
- pip

User also should have account on Azure Portal. 


## Deployment

### Deployment and run on local environment
#### Clone repository and enter cloned project directory:

   ```bash
   $ git clone https://github.com/pmservice/ai-openscale-tutorials
   $ cd ai-openscale-tutorials/applications/custom-ml-engine-azure
   ```
#### Run:

```bash
$ pip install -r requirements.txt
$ export FLASK_APP=app.py
$ python -m flask run
```

Application server will be available at `127.0.0.1:5000`.

#### Test locally:

```bash
$ cd ai-openscale-tutorials/applications/custom-ml-engine-azure/examples
$ python score_credit.py
```

### Deployment and run on Azure Cloud (App Services)

#### Login to Azure Portal and open Cloud Shell Console
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
import requests

APP_URL = <put your app url here>
DEPLOYMENTS_URL = APP_URL + '/v1/deployments'
r = requests.get(DEPLOYMENTS_URL)

print(str(r.text))
```

### Score
Request:
```python
import requests

APP_URL = <put your app url here>
SCORING_URL = APP_URL + '/v1/deployments/credit/online'
payload={'fields': ['CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose', 'LoanAmount', 'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent', 'Sex', 'OthersOnLoan', 'CurrentResidenceDuration', 'OwnsProperty', 'Age', 'InstallmentPlans', 'Housing', 'ExistingCreditsCount', 'Job', 'Dependents', 'Telephone', 'ForeignWorker'], 'values': [['no_checking', 13, 'credits_paid_to_date', 'car_new', 1343, '100_to_500', '1_to_4', 2, 'female', 'none', 3, 'savings_insurance', 25, 'none', 'own', 2, 'skilled', 1, 'none', 'yes'], ['no_checking', 24, 'prior_payments_delayed', 'furniture', 4567, '500_to_1000', '1_to_4', 4, 'male', 'none', 4, 'savings_insurance', 60, 'none', 'free', 2, 'management_self-employed', 1, 'none', 'yes']]}

r = requests.post(SCORING_URL, json=payload)

print(str(r.json()))
```


## References:
1. [AI OpenScale service](https://console.bluemix.net/catalog/services/ai-openscale)
2. [REST API specification](https://aiopenscale-custom-deployement-spec.mybluemix.net/)

