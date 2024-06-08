import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from data_inputer import DataInputer
from risk_assessor import RiskAssessor

class Validator:
    def __init__(self, data_inputer: DataInputer, risk_assessor: RiskAssessor):
        self.__data_inputer = data_inputer
        self.__risk_assessor = risk_assessor
    
    def validate_ds2(self):
        """
        Validate the risk assessment for dataset 4
        """
        X_test, y_test = self.__risk_assessor.ds2_test_data
        self.__validate_dataset(X_test, y_test, 20, "ds2")
        
    def validate_ds4(self):
        """
        Validate the risk assessment for dataset 4
        """
        X_test, y_test = self.__risk_assessor.ds4_test_data
        self.__validate_dataset(X_test, y_test, 100, "ds4")

    def __validate_dataset(self, X_test, y_test, part, ds_name):
        # initialize the mean squared error
        mean_squared_error = 0
        
        # for each row in X_test
        for i in range(len(X_test) // part):
            row = X_test.iloc[i].to_dict()

            # prepare the query by the data inputer
            query = self.__data_inputer.translate_ds_columns_to_standard(ds_name, row)
            validated_data = self.__data_inputer.get_valid_input(query, is_discard_errors=True)
            
            # call calculate_risk and get the risk percentage
            _, risk_percentage = self.__risk_assessor.calculate_risk(validated_data)

            # calculate the squared error between the risk percentage and y_test
            mean_squared_error += (risk_percentage - y_test[i]) ** 2

        # calculate the mean squared error
        return mean_squared_error / len(X_test)