import pandas as pd
import os
import json
from DataInputer import DataInputer
from KNNDataProcessor import KNNDataProcessor
from DS4.DS4PreProcessor import DS4PreProcessor
from DS4.DS4NaiveBayesPredictor import DS4NaiveBayesPredictor

def main():

    with open('./Alpha/common_columns.json') as f:
        common_columns = json.load(f)

    data_processor = DataInputer(common_columns)
    mock_data = data_processor.get_mock_data()
    query_ds2, query_ds4 = data_processor.prepare_queries(mock_data)

    df2 = pd.read_csv('./Alpha/datasets/dataset2.csv')
    df2.name = 'ds2'

    df4 = pd.read_csv('./Alpha/datasets/dataset4.csv')
    ds4_preprocessor = DS4PreProcessor(df4)
    df4 = ds4_preprocessor.preprocessed_df4
    df4.name = 'ds4'

    knn_data_processor_ds2 = KNNDataProcessor(common_columns, df2)
    user_input_processed_df2 = knn_data_processor_ds2.prepare_user_input_for_knn(query_ds2, "ds2")
    nearest_neighbor_row_ds2 = knn_data_processor_ds2.find_nearest_neighbor(user_input_processed_df2)
    print(f"Query for dataset2: {query_ds2}")
    print("Nearest neighbor in dataset2:")
    print(nearest_neighbor_row_ds2)
    print()

    knn_data_processor_ds4 = KNNDataProcessor(common_columns, df4)
    user_input_processed_df4 = knn_data_processor_ds4.prepare_user_input_for_knn(query_ds4, "ds4")
    nearest_neighbor_row_ds4 = knn_data_processor_ds4.find_nearest_neighbor(user_input_processed_df4)
    print(f"Query for dataset4: {query_ds4}")
    print("Nearest neighbor in dataset4:")
    print(nearest_neighbor_row_ds4)
    print()

    
    print("Predicting hospital_death using Naive Bayes on dataset4")
    predictor = DS4NaiveBayesPredictor(df4)
    path = './Alpha/models/DS4NaiveBayesPredictor.pkl'
    if not os.path.exists(path):
        predictor.train_model(path)

    prediction = predictor.predict(nearest_neighbor_row_ds4, path)
    print(f"Prediction: {prediction}")

if __name__ == '__main__':
    main()