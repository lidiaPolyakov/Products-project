import json
from DataInputer import DataInputer
from KNNDataProcessor import KNNDataProcessor
import pandas as pd

def main():

    with open('./Alpha/common_columns.json') as f:
        common_columns = json.load(f)

    data_processor = DataInputer(common_columns)
    mock_data = data_processor.get_mock_data()
    query_ds2, query_ds4 = data_processor.prepare_queries(mock_data)

    df2 = pd.read_csv('./Alpha/datasets/dataset2.csv')
    df2.name = 'ds2'

    df4 = pd.read_csv('./Alpha/datasets/dataset4.csv')
    df4.name = 'ds4'

    knn_data_processor_ds2 = KNNDataProcessor(common_columns, df2)
    user_input_processed_df2 = knn_data_processor_ds2.prepare_user_input_for_knn(query_ds2, "ds2")
    nearest_neighbor_row_ds2 = knn_data_processor_ds2.find_nearest_neighbor(user_input_processed_df2)
    print("Nearest neighbor in dataset2:")
    print(nearest_neighbor_row_ds2)

    knn_data_processor_ds4 = KNNDataProcessor(common_columns, df4)
    user_input_processed_df4 = knn_data_processor_ds4.prepare_user_input_for_knn(query_ds4, "ds4")
    nearest_neighbor_row_ds4 = knn_data_processor_ds4.find_nearest_neighbor(user_input_processed_df4)
    print("Nearest neighbor in dataset4:")
    print(nearest_neighbor_row_ds4)

if __name__ == '__main__':
    main()