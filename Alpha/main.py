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
from ds4.ds4_svm_predictor import DS4SVMPredictor
from ds4.ds4_xgboost_predictor import DS4XGBoostPredictor

from prediction_evaluator import PredictionEvaluator

def run_predictor(target_column, predictor, ds_name, nearest_neighbor_row, evaluator):
    print(f"Predicting {target_column} using {predictor.__class__.__name__} on {ds_name}")
    predictor.train_model()
    prediction = predictor.predict(nearest_neighbor_row)
    evaluation = predictor.evaluate_model()
    evaluator.add_prediction(prediction, evaluation, ds_name)

def ds4(common_columns, df, evaluator, query_ds4):
    knn_data_processor_ds4 = KNNDataProcessor(common_columns, df, query_ds4)
    nearest_neighbor_row_ds4 = knn_data_processor_ds4.find_nearest_neighbor()
    predictors = [
        DS4NNPredictor(df, './Alpha/models/DS4NNPredictor.keras'),
        DS4NaiveBayesPredictor(df, './Alpha/models/DS4NaiveBayesPredictor.pkl'),
        DS4SVMPredictor(df, './Alpha/models/DS4SVMPredictor.pkl'),
        DS4XGBoostPredictor(df, './Alpha/models/DS4XGBoostPredictor.pkl')
    ]
    for predictor in predictors:
        run_predictor('hospital_death', predictor, "ds4", nearest_neighbor_row_ds4, evaluator)

def ds2(common_columns, df, evaluator, query_ds2):
    knn_data_processor_ds2 = KNNDataProcessor(common_columns, df, query_ds2)
    nearest_neighbor_row_ds2 = knn_data_processor_ds2.find_nearest_neighbor()
    predictors = [
        DS2XGBoostPredictor(df, './Alpha/models/DS2XGBoostPredictor.pkl'),
        DS2SVMPredictor(df, './Alpha/models/DS2SVMPredictor.pkl')
    ]
    for predictor in predictors:
        run_predictor('VITAL_STATUS', predictor, "ds2", nearest_neighbor_row_ds2, evaluator)


def calculate_risk(medical_data=None):
    with open('./Alpha/common_columns.json') as f:
        common_columns = json.load(f)
    data_processor = DataInputer(common_columns)

    if medical_data is None:
        validated_data = data_processor.get_mock_data()
    else:
        validated_data = data_processor.get_valid_input(medical_data)

    query_ds2, query_ds4 = data_processor.prepare_queries(validated_data)
    
    df2 = pd.read_csv('./Alpha/datasets/dataset2.csv')
    ds2_preprocessor = DS2PreProcessor(df2)
    df2 = ds2_preprocessor.preprocessed_df2
    df2.name = 'ds2'
    
    df4 = pd.read_csv('./Alpha/datasets/dataset4.csv')
    ds4_preprocessor = DS4PreProcessor(df4)
    df4 = ds4_preprocessor.preprocessed_df4
    df4.name = 'ds4'
    
    evaluator = PredictionEvaluator(
        ds2={
            "doctor_votes": 3,
            "num_rows": ds2_preprocessor.number_of_rows
        },
        ds4={
            "doctor_votes": 3,
            "num_rows": ds4_preprocessor.number_of_rows
        }
    )
    
    ds2(common_columns, df2, evaluator, query_ds2)
    
    ds4(common_columns, df4, evaluator, query_ds4)
    
    risk_assessment = evaluator.evaluate_risk_assessment()
    
    print(f"Risk assessment: {risk_assessment}")
    return risk_assessment

if __name__ == '__main__':
    medical_data = {
        'gender': 'Female',
        'race': 'African American',
        'smoking history': 'Currently smoking',
        'height - cm': 153,
        'weight - kg': 35,
        'age': 110,
        'urine':12.1824
        
    }
    calculate_risk(medical_data)


#Painful Urination: Might reduce output due to discomfort -  50 ml
#Difficulties in Stooling: Does not directly affect urine output, but could indicate dehydration affecting overall fluid balance. - 400 ml
#Frequent Urination: Likely increases output. 2000 ml
#Yellow, Green Discharge: Indicates possible infection, not directly affecting output volume but clinically significant. 2500 ml
