# Custom machine learning engine

## Serving multi-engine models

The repository contains the code for creating custom deployment of  following serve engine and model combinations: 
1. Azure Studio: Three different variations Product Line model. 
   1. A model having `probability`, `prediction` and `predicted-label` as part of the scoring response
   2. A model having `probability` and `predicted-label` as part of the scoring response
   3. A model having only `probability` as part of the scoring response
2. AWS SageMaker: Iris model
3. Watson Machine Learning: SMS Spam Detection Model (unstructured-text)
4. Watson Machine Learning: MNIST Digit Recognition Model (unstructured-image)

Custom deployment provides REST API endpoints to score the above models and to list deployment endpoints.

## Build
1. npm install
2. Setting environment variables:
   1. `export AZURE_APIKEY=<azure api key for deployment>` for Product Line model in our Azure account
   2. `export AWS_ACCESS_KEY_ID=<aws account access key>` for AWS Sagemaker
   3. `export AWS_SECRET_ACCESS_KEY=<aws account secret key>` for AWS Sagemaker
   4. `export WML_USERNAME=<wml username>` for Watson Machine Learning
   5. `export WML_PASSWORD=<wml password>` for Watson Machine Learning
3. npm start
   1. list deployment
     `curl http://localhost:5000/v1/deployments`
   2. scoring
     ```
     curl -XPOST http://localhost:5000/v1/deployments/3e508dbd-0fca-4921-92f5-41fc1a8eabee/online -H "content-type: application/json" -d '{"fields":["GENDER","AGE","MARITAL_STATUS","PROFESSION"],"values":[["M",25,"Single","Professional"]]}'
     
     {"fields":["GENDER","AGE","MARITAL_STATUS","PROFESSION","PRODUCT_LINE","Scored Labels","Scored Probabilities"],"values":[["M","25","Single","Professional","NA","Personal Accessories",[0.290755773151037,0,0.304315949551287,0,0.404928277297676]]]}
     ```

## Deploy
1. COPY manifest.yml.tmp to manifest.yml
1. Edit manifest.yml
1. bx push app

## References:
1. [AI OpenScale service](https://console.bluemix.net/catalog/services/ai-openscale)
2. [REST API specification](https://aiopenscale-custom-deployement-spec.mybluemix.net/)