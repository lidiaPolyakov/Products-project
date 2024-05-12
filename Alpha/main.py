import pandas as pd
import json

from data_inputer import DataInputer
from knn_data_processor import KNNDataProcessor

from ds2.ds2_preprocessor import DS2PreProcessor
from ds2.ds2_xgboost_predictor import DS2XGBoostPredictor
from ds2.ds2_svm_predictor import DS2SVMPredictor

from ds4.ds4_pre_processor import DS4PreProcessor
from ds4.ds4_nn_predictor import DS4NNPredictor
from ds4.ds4_naive_bayes_predictor import DS4NaiveBayesPredictor

from prediction_evaluator import PredictionEvaluator

evaluator = PredictionEvaluator()

def run_predictor(target_column, predictor, ds_name, nearest_neighbor_row):
    print(f"Predicting {target_column} using {predictor.__class__.__name__} on {ds_name}")
    predictor.train_model()
    prediction = predictor.predict(nearest_neighbor_row)
    evaluation = predictor.evaluate_model()
    evaluator.add_prediction(prediction, evaluation)

def ds4(common_columns, query_ds4):
    df4 = pd.read_csv('./Alpha/datasets/dataset4.csv')
    ds4_preprocessor = DS4PreProcessor(df4)
    df4 = ds4_preprocessor.preprocessed_df4
    df4.name = 'ds4'

    knn_data_processor_ds4 = KNNDataProcessor(common_columns, df4, query_ds4)
    nearest_neighbor_row_ds4 = knn_data_processor_ds4.find_nearest_neighbor()

    predictors = [
        DS4NNPredictor(df4, './Alpha/models/DS4NNPredictor.keras'),
        DS4NaiveBayesPredictor(df4, './Alpha/models/DS4NaiveBayesPredictor.pkl'),
        # DS4SVMPredictor(df4, './Alpha/models/DS4SVMPredictor.pkl')
    ]
    for predictor in predictors:
        run_predictor('hospital_death', predictor, "ds4", nearest_neighbor_row_ds4)

def ds2(common_columns, query_ds2):
    df2 = pd.read_csv('./Alpha/datasets/dataset2.csv')
    ds2_preprocessor = DS2PreProcessor(df2)
    df2 = ds2_preprocessor.preprocessed_df2
    df2.name = 'ds2'

    knn_data_processor_ds2 = KNNDataProcessor(common_columns, df2, query_ds2)
    nearest_neighbor_row_ds2 = knn_data_processor_ds2.find_nearest_neighbor()

    predictors = [
        DS2XGBoostPredictor(df2, './Alpha/models/DS2XGBoostPredictor.pkl'),
        DS2SVMPredictor(df2, './Alpha/models/DS2SVMPredictor.pkl')
    ]
    for predictor in predictors:
        run_predictor('VITAL_STATUS', predictor, "ds2", nearest_neighbor_row_ds2)


def calculate_risk(medical_data):
    with open('./Alpha/common_columns.json') as f:
        common_columns = json.load(f)
    data_processor = DataInputer(common_columns)
    validated_data = data_processor.get_valid_input(medical_data)
    query_ds2, query_ds4 = data_processor.prepare_queries(validated_data)
    
    ds2(common_columns, query_ds2)
    
    ds4(common_columns, query_ds4)
    
    risk_assessment = evaluator.evaluate_risk_assessment()
    
    print(f"Risk assessment: {risk_assessment}")
    return risk_assessment

if __name__ == '__main__':
    medical_data = {
        'gender': 'Male',
        'race': 'Caucasian',
        'smoking history': 'Smoked in the past',
        'height - cm': 153,
        'weight - kg': 35,
        'age': 30
    }
    calculate_risk(medical_data)