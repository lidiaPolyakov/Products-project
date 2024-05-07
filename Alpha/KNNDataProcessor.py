import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors

class KNNDataProcessor:
    def __init__(self, common_columns, df):
        self.common_columns = common_columns
        df_copy = df.copy()
        df_copy.name = df.name

        self.label_encoders = {}
        self.scalers = {}
        self.min_max_scalers = np.array([])

        for col_info in self.common_columns:
            datatype = col_info["datatype"]
            column_name = col_info["column"]["name"][df.name]
            if column_name is None:
                continue
            if datatype == "category":
                le = LabelEncoder()
                df_copy[column_name] = le.fit_transform(df_copy[column_name].astype(str))
                self.label_encoders[column_name] = le
                self.min_max_scalers = np.append(self.min_max_scalers, np.nan)
            else:
                scaler = StandardScaler()
                df_copy[column_name] = scaler.fit_transform(df_copy[[column_name]])
                self.scalers[column_name] = scaler
                self.min_max_scalers = np.append(self.min_max_scalers, df_copy[column_name].max() - df_copy[column_name].min())
        self.df_copy = df_copy

    def map_input_to_dataset_value(self, input_value, column_info, dataset_name):
        if column_info["datatype"] == "category":
            return column_info["column"]["categories"][input_value][dataset_name]
        return input_value

    def prepare_user_input_for_knn(self, user_input, dataset_name):
        processed_input = {}
        for col_info in self.common_columns:
            dataset_column_name = col_info["column"]["name"][dataset_name]
            if dataset_column_name is None:
                continue
            if dataset_column_name not in user_input:
                continue

            input_val = user_input[dataset_column_name]
            if col_info["datatype"] == "category":
                mapped_input_val = self.map_input_to_dataset_value(input_val, col_info, dataset_name)
                input_val = self.label_encoders[dataset_column_name].transform([str(mapped_input_val)])[0]
            elif dataset_column_name in self.scalers:
                input_val_df = pd.DataFrame({dataset_column_name: [input_val]})
                input_val = self.scalers[dataset_column_name].transform(input_val_df)[0, 0]

            processed_input[dataset_column_name] = input_val

        return processed_input

    def nearest_neighbor_metric(self, x, y, min_max_scalers):
        categorical = np.isnan(min_max_scalers)
        numeric = ~categorical
        return np.sqrt(
            np.sum(((x[numeric] - y[numeric]) / min_max_scalers[numeric]) ** 2)
            +
            np.sum(x[categorical] != y[categorical])
        )

    def inverse_transform_row(self, row):
        # inverse transform the row to get the original values
        for col_info in self.common_columns:
            dataset_column_name = col_info["column"]["name"][self.df_copy.name]
            if dataset_column_name is None:
                continue
            if col_info["datatype"] == "category":
                row[dataset_column_name] = self.label_encoders[dataset_column_name].inverse_transform([row[dataset_column_name]])[0]
            elif dataset_column_name in self.scalers:
                row[dataset_column_name] = self.scalers[dataset_column_name].inverse_transform([[row[dataset_column_name]]])[0, 0]
        return row
 
    def find_nearest_neighbor(self, user_input_processed):
        relevant_columns = []
        for col_info in self.common_columns:
            dataset_column_name = col_info["column"]["name"][self.df_copy.name]
            if dataset_column_name is None:
                continue
            relevant_columns.append(dataset_column_name)
        df_copy = self.df_copy.dropna(subset=relevant_columns)
        
        intersection_columns = [col for col in relevant_columns if col in user_input_processed]
        
        df_processed_relevant = df_copy[intersection_columns]

        knn = NearestNeighbors(n_neighbors=1, metric=self.nearest_neighbor_metric)
        knn.fit(df_processed_relevant)

        knn_input_df = pd.DataFrame([user_input_processed], columns=intersection_columns)
        nearest_neighbor_index = knn.kneighbors(knn_input_df, return_distance=False)[0][0]

        # get the row of original values for the nearest neighbor
        row = df_copy.iloc[nearest_neighbor_index].copy()

        # replace the nearest neighbor values with the available user input values
        for key in user_input_processed.keys():
            row[key] = user_input_processed[key]

        # inverse transform the row to get the original values
        return self.inverse_transform_row(row)
