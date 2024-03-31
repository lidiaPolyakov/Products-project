from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors

class KNNDataProcessor:
    def __init__(self, common_columns, df):
        self.common_columns = common_columns
        df_copy = df.copy()
        df_copy.name = df.name

        label_encoders = {}
        scalers = {}

        for col_info in self.common_columns:
            datatype = col_info["datatype"]
            column_name = col_info["column"]["name"][df.name]
            if column_name is None:
                continue
            if datatype == "category":
                le = LabelEncoder()
                df_copy[column_name] = le.fit_transform(df_copy[column_name].astype(str))
                label_encoders[column_name] = le
            else:
                scaler = StandardScaler()
                df_copy[column_name] = scaler.fit_transform(df_copy[[column_name]])
                scalers[column_name] = scaler
        self.df_copy = df_copy
        self.label_encoders = label_encoders
        self.scalers = scalers

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
                raise ValueError(f"Missing input for column: {dataset_column_name}")

            input_val = user_input[dataset_column_name]
            if col_info["datatype"] == "category":
                mapped_input_val = self.map_input_to_dataset_value(input_val, col_info, dataset_name)
                input_val = self.label_encoders[dataset_column_name].transform([str(mapped_input_val)])[0]
            elif dataset_column_name in self.scalers:
                input_val = self.scalers[dataset_column_name].transform([[input_val]])[0, 0]

            processed_input[dataset_column_name] = input_val

        return processed_input

    def find_nearest_neighbor(self, user_input_processed):
        relevant_columns = []
        for col_info in self.common_columns:
            dataset_column_name = col_info["column"]["name"][self.df_copy.name]
            if dataset_column_name is None:
                continue
            relevant_columns.append(dataset_column_name)
        df_copy = self.df_copy.dropna(subset=relevant_columns)
        df_processed_relevant = df_copy[relevant_columns]
        knn_input = [list(user_input_processed.values())]

        knn = NearestNeighbors(n_neighbors=1, metric='cosine')
        knn.fit(df_processed_relevant)
        nearest_neighbor_index = knn.kneighbors(knn_input, return_distance=False)[0][0]

        # get the row of original values for the nearest neighbor
        row = df_copy.iloc[nearest_neighbor_index].copy()

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
