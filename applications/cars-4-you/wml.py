from watson_machine_learning_client import WatsonMachineLearningAPIClient
from flask.logging import default_handler, logging
import json
import os
import random
import re

LOGGER = logging.getLogger(os.path.basename(__file__))
LOGGER.setLevel(logging.DEBUG)


class WML:
    def __init__(self, wml_vcap):

        self.client = WatsonMachineLearningAPIClient(wml_vcap.copy())

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

    def get_recommendation(self, request):
        self._validate_field_in_request("deployment", request)
        self._validate_field_in_request("payload", request)

        deployment = request['deployment']
        payload = request['payload']
        satisfaction = payload['Satisfaction']

        scoring_result = self._score_deployment(deployment, self._prepare_payload(payload))

        area_result = self._get_area_from_result(scoring_result)
        action_result = self._get_action_from_result(scoring_result)

        recommendation = {
            "text": ""
        }

        if satisfaction == 0:
            recommendation['text'] = self.negative_templates[random.randint(0, len(self.negative_templates)-1)].format(
                area_result.split(":")[0].lower(), area_result.split(":")[1].lower(), action_result.lower())
        elif satisfaction == 1:
            recommendation['text'] = self.positive_templates[random.randint(
                0, len(self.positive_templates)-1)]
        else:
            LOGGER.error("Satisfaction field was not set properly.")

        LOGGER.debug("Recommendation: {}".format(recommendation))
        return recommendation

    def get_cars4u_deployments(self):
        deployments = []
        for deployment in self._get_deployments():
            deployment_name = deployment['entity']['name']
            if re.match(r'(.*)({})(.*)'.format("CARS4U"), deployment_name, re.IGNORECASE):
                deployments.append(deployment)

        LOGGER.debug("CARS4U deployments: {}".format(deployments))
        return deployments

    def _get_area_from_result(self, scoring_result):
        area_index = scoring_result['fields'].index('predictedAreaLabel')
        area_value = json.dumps(scoring_result['values'][0][area_index]).replace("\"", "")
        LOGGER.debug("Area value in scoring result: {}".format(area_value))
        return area_value

    def _get_action_from_result(self, scoring_result):
        action_index = scoring_result['fields'].index('predictedActionLabel')
        action_value = json.dumps(scoring_result['values'][0][action_index]).replace("\"", "")
        LOGGER.debug("Action value in scoring result: {}".format(action_value))
        return action_value

    def _get_deployments(self):
        deployments = self.client.deployments.get_details()['resources']
        LOGGER.debug("Deployments: {}".format(deployments))
        return deployments

    def _score_deployment(self, deployment, payload):
        scoring_url = deployment['entity']['scoring_url']
        LOGGER.debug("Scoring url: {}".format(scoring_url))
        LOGGER.debug("Scoring payload: {}".format(payload))

        scoring_result = self.client.deployments.score(scoring_url, payload)
        LOGGER.debug("Scoring result: {}".format(scoring_result))
        return scoring_result

    def _prepare_payload(self, request):
        self._validate_field_in_request("Gender", request)
        self._validate_field_in_request("Status", request)
        self._validate_field_in_request("Children", request)
        self._validate_field_in_request("Age", request)
        self._validate_field_in_request("Customer_Status", request)
        self._validate_field_in_request("Car_Owner", request)
        self._validate_field_in_request("Customer_Service", request)
        self._validate_field_in_request("Satisfaction", request)

        fields = ['ID', 'Gender', 'Status', 'Children', 'Age', 'Customer_Status', 'Car_Owner', 'Customer_Service',
                  'Business_Area', 'Satisfaction']

        values = [3785,
                  str(request['Gender']),
                  str(request['Status']),
                  int(request['Children']),
                  int(request['Age']),
                  str(request['Customer_Status']),
                  str(request['Car_Owner']),
                  str(request['Customer_Service']),
                  str('Product: Information'),
                  int(request['Satisfaction'])]

        return {"fields": fields, "values": [values]}

    def _validate_field_in_request(self, field, request):
        if field not in request:
            LOGGER.error("{} is not provided in request json!".format(field))

    # def analyze_business_area(self, request):
    #     LOGGER.info("Scoring Area/Action AI function.")
    #     Gender = request['Gender']
    #     status = request['status']
    #     comment = request['comment']
    #     childrens = int(request['childrens'])
    #     age = int(request['age'])
    #     customer_status = request['customer']
    #     car_owner = request['owner']
    #     satisfaction = request['satisfaction']
    #
    #     fields = ['ID', 'Gender', 'Status', 'Children', 'Age',
    #                 'Customer_Status', 'Car_Owner', 'Customer_Service', 'Satisfaction']
    #     values = [11, Gender, status, childrens, age,
    #                 customer_status, car_owner, comment, int(satisfaction)]
    #
    #     LOGGER.debug("Scoring url: {} ".format(self.area_action_scoring_url))
    #     payload_scoring = {"fields": fields, "values": [values]}
    #     LOGGER.debug("Payload scoring: {}".format(payload_scoring))
    #
    #     scoring = self.client.deployments.score(self.area_action_scoring_url, payload_scoring, transaction_id=self.transaction_id)
    #     LOGGER.debug("Scoring result: {}".format(scoring))
    #
    #     action_index = scoring['fields'].index('Prediction_Action')
    #     action_value = scoring['values'][0][action_index]
    #
    #     area_index = scoring['fields'].index('Prediction_Area')
    #     area_value = scoring['values'][0][area_index]
    #
    #     LOGGER.debug("Predicted area value: {}".format(area_value))
    #     LOGGER.debug("Predicted action value: {}".format(action_value))
    #
    #     client_response = ""
    #     if satisfaction == 0:
    #         client_response = self.negative_templates[random.randint(0, len(self.negative_templates)-1)].format(
    #             area_value.split(":")[0].lower(), area_value.split(":")[1].lower(), action_value.lower())
    #     elif satisfaction == 1:
    #         client_response = self.positive_templates[random.randint(
    #             0, len(self.positive_templates)-1)]
    #     else:
    #         LOGGER.error("Satisfaction field was not set properly.")
    #
    #     return {"client_response": client_response, "action": action_value}
    #
    # def analyze_satisfaction(self, text):
    #     LOGGER.info("Scoring Satisfaction function.")
    #
    #     payload = {
    #         'fields': ['feedback'],
    #         'values': [
    #             ["{}".format(text)]
    #         ]
    #     }
    #
    #     LOGGER.debug("Scoring payload: {}".format(payload))
    #     LOGGER.debug("Scoring url: {}".format(self.satisfaction_scoring_url))
    #     scoring = self.client.deployments.score(self.satisfaction_scoring_url, payload, transaction_id=self.transaction_id)
    #     LOGGER.debug("Scoring result: {}".format(scoring))
    #
    #     sentiment_index = scoring['fields'].index('prediction_classes')
    #     sentiment_value = scoring['values'][0][sentiment_index][0]
    #
    #     LOGGER.debug("Predicted sentiment: {}".format(sentiment_value))
    #     return str(sentiment_value)
    #
    # def get_function_deployments(self, keyword):
    #     LOGGER.info("Getting '{}' function deployments.".format(keyword))
    #     self.deployment_list = self.client.deployments.get_details()['resources']
    #     deployments_array = []
    #
    #     for deployment in self.deployment_list:
    #         deployment_name = deployment['entity']['name']
    #         if re.match(r'(.*)({})(.*)'.format(keyword), deployment_name, re.IGNORECASE) and re.match(r'(.*)(function)(.*)', deployment_name, re.IGNORECASE):
    #             deployments_array.append({
    #                 "name": deployment['entity']['name'],
    #                 "guid": deployment['metadata']['guid']
    #             })
    #     if len(deployments_array) == 0:
    #         for deployment in self.deployment_list:
    #             deployments_array.append({
    #                 "name": deployment['entity']['name'],
    #                 "guid": deployment['metadata']['guid']
    #             })
    #
    #     LOGGER.debug(deployments_array)
    #     return deployments_array
    #
    # def update_scoring_functions(self, deployments=None):
    #     LOGGER.info("Updating scoring functions.")
    #     LOGGER.debug("Saved deployments: {}".format(str(deployments)))
    #     if deployments is None:
    #         self.area_action_deployment_guid = self.get_function_deployments(keyword="area")[0]['guid']
    #         self.satisfaction_deployment_guid = self.get_function_deployments(keyword="satisfaction")[0]['guid']
    #     else:
    #         self.area_action_deployment_guid = deployments["areaaction"]
    #         self.satisfaction_deployment_guid = deployments["satisfaction"]
    #
    #     LOGGER.debug("Area and action deployment guid: {}".format(self.area_action_deployment_guid))
    #     LOGGER.debug("Satisfaction deployment guid: {}".format(self.satisfaction_deployment_guid))
    #
    #     self.area_action_scoring_url = ""
    #     self.satisfaction_scoring_url = ""
    #
    #     for deployment in self.deployment_list:
    #         if self.area_action_deployment_guid == deployment['metadata']['guid']:
    #             self.area_action_scoring_url = deployment['entity']['scoring_url']
    #         elif self.satisfaction_deployment_guid == deployment['metadata']['guid']:
    #             self.satisfaction_scoring_url = deployment['entity']['scoring_url']
    #
    #     LOGGER.debug("Area/Action scoring url: {}".format(self.area_action_scoring_url))
    #     LOGGER.debug("Satisfaction scoring url {}".format(self.satisfaction_scoring_url))

        # if self.area_action_scoring_url == "" :
        #     LOGGER.error("Unable to get scoring url for deployment: {}".format(self.area_action_deployment_guid))
        #     raise Exception("Unable to get scoring url for deployment: {}".format(self.area_action_deployment_guid))
        # if self.satisfaction_scoring_url == "":
        #     LOGGER.error("Unable to get scoring url for deployment: {}".format(self.satisfaction_deployment_guid))
        #     raise Exception("Unable to get scoring url for deployment: {}".format(self.satisfaction_deployment_guid))
