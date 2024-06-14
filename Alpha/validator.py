import pandas as pd
import random
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from data_inputer import DataInputer
from risk_assessor import RiskAssessor

class Validator:
    def __init__(self, data_inputer: DataInputer, risk_assessor: RiskAssessor):
        self.__data_inputer = data_inputer
        self.__risk_assessor = risk_assessor
        
        self.__ckd = pd.read_csv('./Alpha/datasets/validation sets/ckd.csv')
        self.__disease = pd.read_csv('./Alpha/datasets/validation sets/Disease.csv')
    
    def validate_ds2(self):
        """
        Validate the risk assessment for dataset 4
        """
        X_test, y_test = self.__risk_assessor.ds2_test_data
        self.__validate_dataset(X_test, y_test, 5, "ds2")
        
    def validate_ds4(self):
        """
        Validate the risk assessment for dataset 4
        """
        X_test, y_test = self.__risk_assessor.ds4_test_data
        self.__validate_dataset(X_test, y_test, 5, "ds4")

    def validate_ckd(self):
        X_test = self.__ckd.drop("class", axis=1)
        y_test = self.__ckd["class"]
        self.__validate_dataset(X_test, y_test, 5, "ckd")

    def __validate_dataset(self, X_test, y_test, num_of_rows, ds_name, is_random=True):
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
            _, risk_percentage = self.__risk_assessor.calculate_risk(validated_data)

            # calculate the squared error between the risk percentage and y_test
            mean_squared_error += (risk_percentage - y_test[index]) ** 2

            print(f"Iteration {i + 1}: {mean_squared_error / X_test_len}")

        # calculate the mean squared error
        return mean_squared_error / len(X_test)