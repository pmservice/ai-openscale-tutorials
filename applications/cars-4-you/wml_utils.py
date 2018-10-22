from watson_machine_learning_client import WatsonMachineLearningAPIClient
from flask.logging import default_handler, logging
import random
import re
import uuid



class WMLHelper:
    def __init__(self, wml_vcap):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        self.logger.info("Client authentication. Instance id: {}".format(wml_vcap["instance_id"]))
        self.client = WatsonMachineLearningAPIClient(wml_vcap.copy())
        self.deployment_list = self.client.deployments.get_details()['resources']

        self.transaction_id = 'transaction-id-' + uuid.uuid4().hex
        self.logger.info("Transaction ID: {}".format(self.transaction_id))

        self.area_action_deployment_guid = ""
        self.satisfaction_deployment_guid = ""
        self.area_action_scoring_url = ""
        self.satisfaction_scoring_url = ""
    
        self.update_scoring_functions()

        self.neutral_templates = ["We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us.",
                                  "We're very sorry for the trouble you experienced with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us.",
                                  "We sincerely apologize for this experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us.",
                                  "I am very disappointed to hear about your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. In the meantime, we’d like to offer you a <b>{}</b> on your next rental with us."]

        self.negative_templates = ["We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly.",
                                   "We're very sorry for the trouble you experienced with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly.",
                                   "We sincerely apologize for this experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly.",
                                   "I am very disappointed to hear about your experience with Cars4U. We will open a case to investigate the issue with <b>{} {}</b>. Our customer agent will contact you shortly."]

        self.positive_templates = ["We are very happy to have provided you with such a positive experience!",
                                   "We are glad to hear you had such a great experience! ",
                                   "We appreciate your positive review about your recent experience with us!"]

    def analyze_business_area(self, request):
        self.logger.info("Scoring Area/Action AI function.")
        gender = request['gender']
        status = request['status']
        comment = request['comment']
        childrens = int(request['childrens'])
        age = int(request['age'])
        customer_status = request['customer']
        car_owner = request['owner']
        satisfaction = request['satisfaction']

        fields = ['ID', 'Gender', 'Status', 'Children', 'Age',
                    'Customer_Status', 'Car_Owner', 'Customer_Service', 'Satisfaction']
        values = [11, gender, status, childrens, age,
                    customer_status, car_owner, comment, int(satisfaction)]

        self.logger.debug("Scoring url: {} ".format(self.area_action_scoring_url))
        payload_scoring = {"fields": fields, "values": [values]}
        self.logger.debug("Payload scoring: {}".format(payload_scoring))

        scoring = self.client.deployments.score(self.area_action_scoring_url, payload_scoring, transaction_id=self.transaction_id)
        self.logger.debug("Scoring result: {}".format(scoring))
        
        action_index = scoring['fields'].index('Prediction_Action')
        action_value = scoring['values'][0][action_index]

        area_index = scoring['fields'].index('Prediction_Area')
        area_value = scoring['values'][0][area_index]
        
        self.logger.debug("Predicted area value: {}".format(area_value))
        self.logger.debug("Predicted action value: {}".format(action_value))

        client_response = ""
        if satisfaction == 0:
            client_response = self.negative_templates[random.randint(0, len(self.negative_templates)-1)].format(
                area_value.split(":")[0].lower(), area_value.split(":")[1].lower(), action_value.lower())
        elif satisfaction == 1:
            client_response = self.positive_templates[random.randint(
                0, len(self.positive_templates)-1)]
        else:
            self.logger.error("Satisfaction field was not set properly.")

        return {"client_response": client_response, "action": action_value}

    def analyze_satisfaction(self, text):
        self.logger.info("Scoring Satisfaction function.")

        payload = {
            'fields': ['feedback'],
            'values': [
                ["{}".format(text)]
            ]
        }

        self.logger.debug("Scoring payload: {}".format(payload))
        self.logger.debug("Scoring url: {}".format(self.satisfaction_scoring_url))
        scoring = self.client.deployments.score(self.satisfaction_scoring_url, payload, transaction_id=self.transaction_id)
        self.logger.debug("Scoring result: {}".format(scoring))

        sentiment_index = scoring['fields'].index('prediction_classes')
        sentiment_value = scoring['values'][0][sentiment_index][0]

        self.logger.debug("Predicted sentiment: {}".format(sentiment_value))
        return str(sentiment_value)

    def get_function_deployments(self, keyword):
        self.logger.info("Getting '{}' function deployments.".format(keyword))
        self.deployment_list = self.client.deployments.get_details()['resources']
        deployments_array = []

        for deployment in self.deployment_list:
            deployment_name = deployment['entity']['name']
            if re.match(r'(.*)({})(.*)'.format(keyword), deployment_name, re.IGNORECASE) and re.match(r'(.*)(function)(.*)', deployment_name, re.IGNORECASE):
                deployments_array.append({
                    "name": deployment['entity']['name'],
                    "guid": deployment['metadata']['guid']
                })
        if len(deployments_array) == 0:
            for deployment in self.deployment_list:
                deployments_array.append({
                    "name": deployment['entity']['name'],
                    "guid": deployment['metadata']['guid']
                })
        
        self.logger.debug(deployments_array)
        return deployments_array

    def update_scoring_functions(self, deployments=None):
        self.logger.info("Updating scoring functions.")
        self.logger.debug("Saved deployments: {}".format(str(deployments)))
        if deployments is None:
            self.area_action_deployment_guid = self.get_function_deployments(keyword="area")[0]['guid']
            self.satisfaction_deployment_guid = self.get_function_deployments(keyword="satisfaction")[0]['guid']
        else:
            self.area_action_deployment_guid = deployments["areaaction"]
            self.satisfaction_deployment_guid = deployments["satisfaction"]

        self.logger.debug("Area and action deployment guid: {}".format(self.area_action_deployment_guid))
        self.logger.debug("Satisfaction deployment guid: {}".format(self.satisfaction_deployment_guid))

        self.area_action_scoring_url = "" 
        self.satisfaction_scoring_url = ""
        
        for deployment in self.deployment_list:
            if self.area_action_deployment_guid == deployment['metadata']['guid']:
                self.area_action_scoring_url = deployment['entity']['scoring_url']
            elif self.satisfaction_deployment_guid == deployment['metadata']['guid']:
                self.satisfaction_scoring_url = deployment['entity']['scoring_url']

        self.logger.debug("Area/Action scoring url: {}".format(self.area_action_scoring_url))
        self.logger.debug("Satisfaction scoring url {}".format(self.satisfaction_scoring_url))

        if self.area_action_scoring_url == "" :
            self.logger.error("Unable to get scoring url for deployment: {}".format(self.area_action_deployment_guid))
            raise Exception("Unable to get scoring url for deployment: {}".format(self.area_action_deployment_guid))
        if self.satisfaction_scoring_url == "":
            self.logger.error("Unable to get scoring url for deployment: {}".format(self.satisfaction_deployment_guid))
            raise Exception("Unable to get scoring url for deployment: {}".format(self.satisfaction_deployment_guid))

        