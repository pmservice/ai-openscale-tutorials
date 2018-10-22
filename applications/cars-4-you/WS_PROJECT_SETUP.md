# How to setup the Watson Studio project
The sample application requires machine learning models trained and deployed using Watson Studio. 
Please find step by step instruction below.

## Project configuration
- create project in [Watson Studio](dataplatform.cloud.ibm.com)
- assosiate: Watson Machine Learning and Spark service

## Training data set
- upload the [training data set](https://raw.githubusercontent.com/pmservice/wml-sample-models/master/spark/cars-4-you/data/car_rental_training_data.csv) to DB2 Warehouse on Cloud
- in the Watson Studio create a connection to the table 

## Feedback data set and learning system
- upload the [feedback data set](https://raw.githubusercontent.com/pmservice/wml-sample-models/master/spark/cars-4-you/data/car_rental_feedback_data.csv) to DB2 Warehouse on Cloud
- in the Watson Studio create a connection to the table 

## Notebook to train a model, deploy and configure payload logging
- upload a [notebook](https://dataplatform.ibm.com/analytics/notebooks/v2/5b767931-5a0e-4a03-b8bb-a34562813b0a/view?access_token=af146a6fe880b0fd8afa60affc21b3f2e7658726239e93f60e0d31a233457046) to Watson Studio project

**Note:** Use Spark runtime when uplaoding the notebook

- use `insert to code as spark df` feature to insert the training data table connection (cell [2])
- replace the postgress sql database connection in payload logging section of the notebook (cell [87])
- replace wml_credentials
- run the notebook 

## Configure the learning system
- in the Evaluation section of the model configure learning system by providing connection to feedback table
- set the retrain option to always, redeploy if better
- run new iteration

## Payload logging table and lineage
- in the studio add new connection to the payload logging table to see all scoring results logged
- the lineage can be seen on the lineage tab of the model details


