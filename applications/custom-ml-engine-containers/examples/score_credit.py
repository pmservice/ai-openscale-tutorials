import requests

SERVER_HTTP = 'http://0.0.0.0:5000'
SCORING_CREDIT_ENDPOINT = SERVER_HTTP + '/v1/deployments/credit/online'


def prepare_payload():
    fields = ["CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose", "LoanAmount", "ExistingSavings",
              "EmploymentDuration", "InstallmentPercent", "Sex", "OthersOnLoan", "CurrentResidenceDuration",
              "OwnsProperty", "Age", "InstallmentPlans", "Housing", "ExistingCreditsCount", "Job", "Dependents",
              "Telephone", "ForeignWorker"]
    values = [
        ["no_checking", 13, "credits_paid_to_date", "car_new", 1343, "100_to_500", "1_to_4", 2, "female", "none", 3,
         "savings_insurance", 25, "none", "own", 2, "skilled", 1, "none", "yes"],
        ["no_checking", 24, "prior_payments_delayed", "furniture", 4567, "500_to_1000", "1_to_4", 4, "male", "none",
         4, "savings_insurance", 60, "none", "free", 2, "management_self-employed", 1, "none", "yes"],
        ["0_to_200", 26, "all_credits_paid_back", "car_new", 863, "less_100", "less_1", 2, "female", "co-applicant",
         2, "real_estate", 38, "none", "own", 1, "skilled", 1, "none", "yes"],
        ["0_to_200", 14, "no_credits", "car_new", 2368, "less_100", "1_to_4", 3, "female", "none", 3, "real_estate",
         29, "none", "own", 1, "skilled", 1, "none", "yes"]
    ]

    return {"fields": fields, "values": values}


def main():
    print("\n\n******************************************")
    print("Prepare scoring payload ...")
    payload = prepare_payload()

    print("Score the model ...")
    r = requests.post(SCORING_CREDIT_ENDPOINT, json=payload)

    print("Return predictions ...\n")
    print(str(r.json()))
    print("\n******************************************\n")


if __name__ == "__main__":
    main()
