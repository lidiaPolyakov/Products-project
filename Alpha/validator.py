import pandas as pd
import random
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from data_inputer import DataInputer
from risk_assessor import RiskAssessor

pd.set_option('future.no_silent_downcasting', True)

class Validator:
    def __init__(self, data_inputer: DataInputer, risk_assessor: RiskAssessor):
        self.__data_inputer = data_inputer
        self.__risk_assessor = risk_assessor
        
        self.__ckd = pd.read_csv('./Alpha/datasets/validation sets/ckd.csv')
        self.__disease = pd.read_csv('./Alpha/datasets/validation sets/Disease.csv')
    
    def validate_ds2(self, votes):
        """
        Validate the risk assessment for dataset 2 with specified doctor votes
        """
        X_test, y_test = self.__risk_assessor.ds2_test_data
        return self.__validate_dataset(X_test, y_test, 5, "ds2", votes)
        
    def validate_ds4(self, votes):
        """
        Validate the risk assessment for dataset 4 with specified doctor votes
        """
        X_test, y_test = self.__risk_assessor.ds4_test_data
        return self.__validate_dataset(X_test, y_test, 5, "ds4", votes)

    def validate_ckd(self, votes):
        """
        Validate the risk assessment for ckd with specified doctor votes
        """
        X_test = self.__ckd.drop("class", axis=1)
        y_test = self.__ckd["class"].replace({"ckd": 1, "notckd": 0})
        return self.__validate_dataset(X_test, y_test, 5, "ckd", votes)


    def __validate_dataset(self, X_test, y_test, num_of_rows, ds_name, votes, is_random=False):
        ds2_vote, ds4_vote = votes

        # initialize the mean squared error
        mean_squared_error = 0
        
        X_test_len = len(X_test)
        
        # for each row in X_test
        for i in range(num_of_rows):
            index = random.randint(0, X_test_len - 1) if is_random else i
            row = X_test.iloc[index].to_dict()

            # prepare the query by the data inputer
            query = self.__data_inputer.translate_ds_columns_to_standard(ds_name, row)
            validated_data = self.__data_inputer.get_valid_input(query, is_discard_errors=True)
            
            # call calculate_risk and get the risk percentage
            _, risk_percentage, _ = self.__risk_assessor.calculate_risk(validated_data, ds2_doctor_vote=ds2_vote, ds4_doctor_vote=ds4_vote)

            # calculate the squared error between the risk percentage and y_test
            mean_squared_error += (risk_percentage - y_test[index]) ** 2

            print(f"Iteration {i + 1}: {mean_squared_error / (i + 1)}")

        # calculate the mean squared error
        return mean_squared_error / len(X_test)

    def validate_scenarios(self):
        scenarios = [
            (0, 5),
            (5, 0),
            (3, 3),
            (1, 4),
            (4, 1)
        ]
        
        results = []
        
        for votes in scenarios:
            mse_ds2 = self.validate_ds2(votes)
            mse_ds4 = self.validate_ds4(votes)
            mse_ckd = self.validate_ckd(votes)
            
            results.append({
                "Votes": f"{votes[0]} - {votes[1]}",
                "ds2": mse_ds2,
                "ds4": mse_ds4,
                "ckd": mse_ckd
            })
        
        return pd.DataFrame(results).set_index("Votes")