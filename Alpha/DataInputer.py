import random

class DataInputer:
    def __init__(self, common_columns):
        self.common_columns = common_columns

    def show_category_options(self, allowed_categories):
        print("Options:")
        for category in allowed_categories:
            print(f"- {category}")

    def validate_category_input(self, input_value, allowed_categories):
        return input_value in allowed_categories

    def validate_int_input(self, input_value, value_range):
        try:
            value = int(input_value)
            return value_range[0] <= value <= value_range[1]
        except ValueError:
            return False

    def validate_float_input(self, input_value, value_range):
        try:
            value = float(input_value)
            return value_range[0] <= value <= value_range[1]
        except ValueError:
            return False

    def get_valid_input(self):
        user_inputs = {}
        for column in self.common_columns:
            datatype = column["datatype"]
            column_name = column["standard_column_name"]
            valid_input = False
            
            while not valid_input:
                if datatype == "category":
                    print("Options:")
                    allowed_categories = column["standard_input_values"]["categories"]
                    for category in allowed_categories:
                        print(f"- {category}")

                user_input = input(f"Enter {column_name}: ")

                if datatype == "category":
                    allowed_categories = column["standard_input_values"]["categories"]
                    valid_input = self.validate_category_input(user_input, allowed_categories)
                elif datatype == "int":
                    allowed_range = column["standard_input_values"]["range"]
                    valid_input = self.validate_int_input(user_input, allowed_range)
                elif datatype == "float":
                    allowed_range = column["standard_input_values"]["range"]
                    valid_input = self.validate_float_input(user_input, allowed_range)

                if not valid_input:
                    print(f"Invalid input for {column_name}. Please try again.")
            user_inputs[column_name] = user_input

        return user_inputs

    def get_mock_data(self):
        mock_inputs = {}
        for column in self.common_columns:
            datatype = column["datatype"]
            column_name = column["standard_column_name"]

            if datatype == "category":
                allowed_categories = column["standard_input_values"]["categories"]
                mock_inputs[column_name] = random.choice(allowed_categories)
            elif datatype == "int":
                mock_inputs[column_name] = random.randint(column["standard_input_values"]["range"][0], column["standard_input_values"]["range"][1])
            elif datatype == "float":
                mock_inputs[column_name] = "%.1f" % random.uniform(column["standard_input_values"]["range"][0], column["standard_input_values"]["range"][1])

        return mock_inputs

    def prepare_queries(self, input_columns):
        query_for_ds2 = {}
        query_for_ds4 = {}
        for input_column, common_column in zip(input_columns, self.common_columns):
            if input_column != common_column["standard_column_name"]: continue
            
            df2_column_name = common_column["column"]["name"]["ds2"]
            if df2_column_name is not None:
                query_for_ds2[df2_column_name] = input_columns[input_column]
            
            df4_column_name = common_column["column"]["name"]["ds4"]
            if df4_column_name is not None:
                query_for_ds4[df4_column_name] = input_columns[input_column]

        return query_for_ds2, query_for_ds4
