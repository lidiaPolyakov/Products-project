import json
from DataInputer import DataInputer

def main():

    with open('./Alpha/common_columns.json') as f:
        common_columns = json.load(f)

    data_processor = DataInputer(common_columns)
    mock_data = data_processor.get_mock_data()
    query_ds2, query_ds4 = data_processor.prepare_queries(mock_data)

if __name__ == '__main__':
    main()