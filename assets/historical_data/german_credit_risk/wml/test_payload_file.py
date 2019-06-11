import json

fns = ['history_payloads_{}.json'.format(i) for i in range(7)]

request_fields = set(['CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose', 'LoanAmount', 'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent', 'Sex', 'OthersOnLoan', 'CurrentResidenceDuration', 'OwnsProperty', 'Age', 'InstallmentPlans', 'Housing', 'ExistingCreditsCount', 'Job', 'Dependents', 'Telephone', 'ForeignWorker'])

response_fields = set(['CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose', 'LoanAmount', 'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent', 'Sex', 'OthersOnLoan', 'CurrentResidenceDuration', 'OwnsProperty', 'Age', 'InstallmentPlans', 'Housing', 'ExistingCreditsCount', 'Job', 'Dependents', 'Telephone', 'ForeignWorker', 'CheckingStatus_IX', 'CreditHistory_IX', 'EmploymentDuration_IX', 'ExistingSavings_IX', 'ForeignWorker_IX', 'Housing_IX', 'InstallmentPlans_IX', 'Job_IX', 'LoanPurpose_IX', 'OthersOnLoan_IX', 'OwnsProperty_IX', 'Sex_IX', 'Telephone_IX', 'features', 'rawPrediction', 'probability', 'prediction', 'predictedLabel'])

def test_payload(payload_data, fn):
    print('Test file: ', fn)
    for i, rec in enumerate(payload_data):
        rec_request_fields = set(rec['request']['fields'])
        rec_response_fields = set(rec['response']['fields'])
        n_req = len(request_fields.symmetric_difference(rec_request_fields))
        n_resp = len(response_fields.symmetric_difference(rec_response_fields))
        if (n_req > 0) or (n_resp > 0):
            print(i, n_req, n_resp)

for fn in fns:
    with open(fn) as f:
        payload_data = json.load(f)
        test_payload(payload_data, fn)

