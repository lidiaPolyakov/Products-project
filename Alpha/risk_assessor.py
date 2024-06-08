import pandas as pd
import json

from data_inputer import DataInputer

from ds2.ds2_preprocessor import DS2PreProcessor
from ds4.ds4_pre_processor import DS4PreProcessor

from ds2.ds2_xgboost_predictor import DS2XGBoostPredictor
from ds2.ds2_svm_predictor import DS2SVMPredictor
from ds2.ds2_extra_tree_predictor import DS2ExtraTreePredictor
from ds2.ds2_decision_tree_predictor import DS2DecisionTreePredictor

from ds4.ds4_nn_predictor import DS4NNPredictor
from ds4.ds4_naive_bayes_predictor import DS4NaiveBayesPredictor
from ds4.ds4_svm_predictor import DS4SVMPredictor
from ds4.ds4_xgboost_predictor import DS4XGBoostPredictor

from knn_data_processor import KNNDataProcessor

from prediction_evaluator import PredictionEvaluator

class RiskAssessor:
    def __init__(self, ds2_doctor_vote=1, ds4_doctor_vote=1):
        with open('./Alpha/common_columns.json') as f:
            self.__common_columns = json.load(f)
        self.__data_inputer = DataInputer(self.__common_columns)
        
        df2 = pd.read_csv('./Alpha/datasets/dataset2.csv')
        self.__ds2_preprocessor = DS2PreProcessor(df2)
        
        df4 = pd.read_csv('./Alpha/datasets/dataset4.csv')
        self.__ds4_preprocessor = DS4PreProcessor(df4)
        
        self.__evaluator = PredictionEvaluator(
            ds2={ "doctor_votes": ds2_doctor_vote, "num_rows": self.__ds2_preprocessor.number_of_rows() },
            ds4={ "doctor_votes": ds4_doctor_vote, "num_rows": self.__ds4_preprocessor.number_of_rows() }
        )

    def calculate_risk(self, query=None):
        if query is None:
            validated_data = self.__data_inputer.get_mock_data()
        else:
            validated_data = self.__data_inputer.get_valid_input(query)

        self.__query_ds2, self.__query_ds4 = self.__data_inputer.prepare_queries(validated_data)

        self.__ds2(self.__common_columns, self.__ds2_preprocessor, self.__evaluator, self.__query_ds2)
        self.__ds4(self.__common_columns, self.__ds4_preprocessor, self.__evaluator, self.__query_ds4)

        return self.__evaluator.evaluate_risk_assessment()

    def __ds2(self, common_columns, preprocessor, evaluator, query_ds2):
        knn_data_processor_ds2 = KNNDataProcessor(common_columns, preprocessor.get_preprocessed_data, "ds2", query_ds2)
        nearest_neighbor_row_ds2 = knn_data_processor_ds2.find_nearest_neighbor()
        predictors = [
            DS2XGBoostPredictor(preprocessor, './Alpha/models/DS2XGBoostPredictor.pkl'),
            DS2SVMPredictor(preprocessor, './Alpha/models/DS2SVMPredictor.pkl'),
            DS2ExtraTreePredictor(preprocessor, './Alpha/models/DS2ExtraTreePredictor.keras'),
            DS2DecisionTreePredictor(preprocessor, './Alpha/models/DS2DecisionTreePredictor.pkl')
        ]
        for predictor in predictors:
            self.__run_predictor('VITAL_STATUS', predictor, "ds2", nearest_neighbor_row_ds2, evaluator)

    def __ds4(self, common_columns, preprocessor, evaluator, query_ds4):
        knn_data_processor_ds4 = KNNDataProcessor(common_columns, preprocessor.get_preprocessed_data, "ds4", query_ds4)
        nearest_neighbor_row_ds4 = knn_data_processor_ds4.find_nearest_neighbor()
        predictors = [
            DS4NNPredictor(preprocessor, './Alpha/models/DS4NNPredictor.keras'),
            DS4NaiveBayesPredictor(preprocessor, './Alpha/models/DS4NaiveBayesPredictor.pkl'),
            DS4SVMPredictor(preprocessor, './Alpha/models/DS4SVMPredictor.pkl'),
            DS4XGBoostPredictor(preprocessor, './Alpha/models/DS4XGBoostPredictor.pkl')
        ]
        for predictor in predictors:
            self.__run_predictor('hospital_death', predictor, "ds4", nearest_neighbor_row_ds4, evaluator)
    
    def __run_predictor(self, target_column, predictor, ds_name, nearest_neighbor_row, evaluator):
        print(f"Predicting {target_column} using {predictor.__class__.__name__} on {ds_name}")
        predictor.train_model()
        prediction = predictor.predict(nearest_neighbor_row)
        evaluation = predictor.evaluate_model()
        evaluator.add_prediction(prediction, evaluation, ds_name)