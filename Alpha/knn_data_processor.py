import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors

import time

class KNNDataProcessor:
    def __init__(self, common_columns, df, df_name, user_input):
        self.common_columns = common_columns
        self.user_input = user_input
        self.df_copy = df.copy()
        self.df_name = df_name
        self.dtypes = self.df_copy.dtypes.copy()

        self.label_encoders = {}
        self.scalers = {}
        self.min_max_scalers = np.array([])
        self.min_frequancies = np.array([])
        
        self.max_freq_matrices = []
        self.frequency_of_each_value = []

        self.processed_input = {}

        for col_info in self.common_columns:
            datatype = col_info["datatype"]
            column_name = col_info["column"]["name"][self.df_name]
            if column_name is None:
                continue
            if column_name not in self.user_input:
                continue
            
            if datatype == "category":
                le = LabelEncoder()
                self.df_copy[column_name] = le.fit_transform(self.df_copy[column_name].astype(str))
                self.label_encoders[column_name] = le
                self.min_max_scalers = np.append(self.min_max_scalers, np.nan)

                self.min_frequancies = np.append(self.min_frequancies, self.df_copy[column_name].value_counts().min())

                frequency = self.df_copy[column_name].dropna().value_counts()
                unique_values = frequency.index

                self.frequency_of_each_value.append(frequency)

                max_freq_matrix = pd.DataFrame(index=unique_values, columns=unique_values)
                for value1 in unique_values:
                    for value2 in unique_values:
                        max_freq_matrix.loc[value1, value2] = max(frequency[value1], frequency[value2])
                self.max_freq_matrices.append(max_freq_matrix)

                input_val = user_input[column_name]
                mapped_input_val = self.map_input_to_dataset_value(input_val, col_info, self.df_name)
                input_val = self.label_encoders[column_name].transform([str(mapped_input_val)])[0]
            else:
                scaler = StandardScaler()
                self.df_copy[column_name] = scaler.fit_transform(self.df_copy[[column_name]])
                self.scalers[column_name] = scaler
                self.min_max_scalers = np.append(self.min_max_scalers, self.df_copy[column_name].max() - self.df_copy[column_name].min())

                input_val = user_input[column_name]
                input_val_df = pd.DataFrame({column_name: [input_val]})
                input_val = self.scalers[column_name].transform(input_val_df)[0, 0]
            
            self.processed_input[column_name] = input_val


    def map_input_to_dataset_value(self, input_value, column_info, dataset_name):
        if column_info["datatype"] == "category":
            return column_info["column"]["categories"][input_value][dataset_name]
        return input_value

    def nearest_neighbor_metric(self, x, y):
        # is nan for categorical columns
        categorical = np.isnan(self.min_max_scalers)
        
        # if not nan, then it is numeric
        numeric = ~categorical
        
        # numerical distance calculated using min-max scaling
        numeric_distance = np.sum(((x[numeric] - y[numeric]) / self.min_max_scalers[numeric]) ** 2)
        
        # calculate categorical distance
        categorical_distance = 0
        x_categorical = x[categorical]
        y_categorical = y[categorical]
        
        for i in range(categorical.sum()):
            if x_categorical[i] != y_categorical[i]:
                x_category = x_categorical[i]
                y_category = y_categorical[i]
                max_freq = self.max_freq_matrices[i].loc[x_category, y_category]
                min_freq_of_col = self.min_frequancies[i]
                frequency_of_x_i = self.frequency_of_each_value[i][x_category]
                frequency_of_y_i = self.frequency_of_each_value[i][y_category]
                categorical_distance += (
                    abs(frequency_of_x_i - frequency_of_y_i) + min_freq_of_col
                ) / max_freq
        
        return (numeric_distance + categorical_distance) ** 0.5

    def inverse_transform_row(self, row):
        # inverse transform the row to get the original values
        for col_info in self.common_columns:
            dataset_column_name = col_info["column"]["name"][self.df_name]
            if dataset_column_name is None:
                continue
            if col_info["datatype"] == "category" and dataset_column_name in self.label_encoders:
                row[dataset_column_name] = self.label_encoders[dataset_column_name].inverse_transform([row[dataset_column_name]])[0]
            elif dataset_column_name in self.scalers:
                row[dataset_column_name] = self.scalers[dataset_column_name].inverse_transform([[row[dataset_column_name]]])[0, 0]
        return row
 
    def __evaluate_nearest_neighbors(self, nearest_neighbors_rows):
        """
        Evaluate the nearest neighbors rows to find the mean of
        the numerical columns and the mode of the categorical columns
        Args:
            nearest_neighbors_rows (pd.Dataframe): Dataframe containing the nearest neighbors rows
        Returns:
            pd.Dataframe: Dataframe containing the mean of the numerical columns and the mode of the categorical columns
        """
        
        # save the original order of the columns
        columns_order = nearest_neighbors_rows.columns
        
        for column in self.dtypes.index:
            if isinstance(self.dtypes[column], pd.CategoricalDtype):
                nearest_neighbors_rows[column] = nearest_neighbors_rows[column].astype("category")
            else:
                nearest_neighbors_rows[column] = nearest_neighbors_rows[column].astype(self.dtypes[column])
        
        # Identify the indices for which the data type is category
        category_columns = nearest_neighbors_rows.dtypes == 'category'

        # Select the column names where the data type is category
        category_column_names = category_columns[category_columns].index.tolist()
        
        # Find the mode of the categorical columns
        mode = nearest_neighbors_rows[category_column_names].mode().iloc[0].astype('object')
        
        # Identify the indices for which the data type is numeric
        numeric_columns = nearest_neighbors_rows.dtypes != 'category'

        # Select the column names where the data type is 'category'
        numeric_column_names = numeric_columns[numeric_columns].index.tolist()
        
        # Find the mean of the numerical columns
        mean = nearest_neighbors_rows[numeric_column_names].mean()
        
        # return the mode and mean values in the same order as the input dataframe
        return pd.concat([mode, mean]).reindex(columns_order)

    def find_nearest_neighbor(self, n_neighbors=5):
        relevant_columns = []
        for col_info in self.common_columns:
            dataset_column_name = col_info["column"]["name"][self.df_name]
            if dataset_column_name is None:
                continue
            relevant_columns.append(dataset_column_name)
        df_copy = self.df_copy.dropna(subset=relevant_columns)
        
        intersection_columns = [col for col in relevant_columns if col in self.processed_input]
        
        df_processed_relevant = df_copy[intersection_columns]
        if df_processed_relevant.empty: return None

        knn = NearestNeighbors(n_neighbors=n_neighbors, algorithm='brute', metric=self.nearest_neighbor_metric)
        knn.fit(df_processed_relevant)

        knn_input_df = pd.DataFrame([self.processed_input], columns=intersection_columns)
        
        start = time.time()
        
        nearest_neighbors_indices = knn.kneighbors(knn_input_df, return_distance=False)[0]
        
        end = time.time()
        
        print(f"Time taken to find nearest neighbors: {end - start} seconds")

        # get the row of original values for the nearest neighbor
        rows = df_copy.iloc[nearest_neighbors_indices].copy()
        
        # evaluate the nearest neighbors to get the mean of the
        # numerical columns and the mode of the categorical columns
        row = self.__evaluate_nearest_neighbors(rows)

        # replace the nearest neighbor values with the available user input values
        for key in self.processed_input.keys():
            row[key] = self.processed_input[key]

        # inverse transform the row to get the original values
        return self.inverse_transform_row(row)
