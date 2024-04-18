import pandas as pd
import os
import json
from DataInputer import DataInputer
from KNNDataProcessor import KNNDataProcessor

from DS2.DS2PreProcessor import DS2PreProcessor
from DS2.DS2XGBoostPredictor import DS2XGBoostPredictor
from DS2.DS2SVMPredictor import DS2SVMPredictor

from DS4.DS4PreProcessor import DS4PreProcessor
from DS4.DS4NNPredictor import DS4NNPredictor
from DS4.DS4NaiveBayesPredictor import DS4NaiveBayesPredictor
from DS4.DS4SVMPredictor import DS4SVMPredictor

def run_predictor(target_column, predictor, ds_name, nearest_neighbor_row):
    print(f"Predicting {target_column} using {predictor.__class__.__name__} on {ds_name}")
    predictor.train_model()
    prediction = predictor.predict(nearest_neighbor_row)
    print(f"Prediction: {prediction}")
    print(f"Evaluation: {predictor.evaluate_model()}")

def ds4(common_columns, query_ds4):
    df4 = pd.read_csv('./Alpha/datasets/dataset4.csv')
    ds4_preprocessor = DS4PreProcessor(df4)
    df4 = ds4_preprocessor.preprocessed_df4
    df4.name = 'ds4'

    knn_data_processor_ds4 = KNNDataProcessor(common_columns, df4)
    user_input_processed_df4 = knn_data_processor_ds4.prepare_user_input_for_knn(query_ds4, "ds4")
    nearest_neighbor_row_ds4 = knn_data_processor_ds4.find_nearest_neighbor(user_input_processed_df4)
    print(f"Query for dataset4: {query_ds4}")
    print("Nearest neighbor in dataset4:")
    print(nearest_neighbor_row_ds4)
    print()

    predictors = [
        DS4NNPredictor(df4, './Alpha/models/DS4NNPredictor.keras'),
        DS4NaiveBayesPredictor(df4, './Alpha/models/DS4NaiveBayesPredictor.pkl'),
        DS4SVMPredictor(df4, './Alpha/models/DS4SVMPredictor.pkl')
    ]
    for predictor in predictors:
        run_predictor('hospital_death', predictor, "ds4", nearest_neighbor_row_ds4)

def ds2(common_columns, query_ds2):
    df2 = pd.read_csv('./Alpha/datasets/dataset2.csv')
    ds2_preprocessor = DS2PreProcessor(df2)
    df2 = ds2_preprocessor.preprocessed_df2
    df2.name = 'ds2'

    knn_data_processor_ds2 = KNNDataProcessor(common_columns, df2)
    user_input_processed_df2 = knn_data_processor_ds2.prepare_user_input_for_knn(query_ds2, "ds2")
    nearest_neighbor_row_ds2 = knn_data_processor_ds2.find_nearest_neighbor(user_input_processed_df2)
    print(f"Query for dataset2: {query_ds2}")
    print("Nearest neighbor in dataset2:")
    print(nearest_neighbor_row_ds2)
    print()

    predictors = [
        DS2XGBoostPredictor(df2, './Alpha/models/DS2XGBoostPredictor.pkl'),
        DS2SVMPredictor(df2, './Alpha/models/DS2SVMPredictor.pkl')
    ]
    for predictor in predictors:
        run_predictor('VITAL_STATUS', predictor, "ds2", nearest_neighbor_row_ds2)


def main():
    with open('./Alpha/common_columns.json') as f:
        common_columns = json.load(f)
    data_processor = DataInputer(common_columns)
    mock_data = data_processor.get_mock_data()
    query_ds2, query_ds4 = data_processor.prepare_queries(mock_data)
    
    ds2(common_columns, query_ds2)
    
    ds4(common_columns, query_ds4)

if __name__ == '__main__':
    main()