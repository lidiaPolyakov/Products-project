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

    def get_valid_input(self, data_input):
        user_inputs = {}
        errors = {}

        for column in self.common_columns:
            datatype = column["datatype"]
            column_name = column["standard_column_name"]
            
            if column_name == 'vital status':
                continue
            if column_name not in data_input:
                errors[column_name] = "This field is required."
                continue

            user_input = data_input[column_name]

            if datatype == "category":
                allowed_categories = column["standard_input_values"]["categories"]
                if not self.validate_category_input(user_input, allowed_categories):
                    errors[column_name] = f"Invalid category. Allowed options: {', '.join(allowed_categories)}"
            elif datatype == "int":
                allowed_range = column["standard_input_values"]["range"]
                if not self.validate_int_input(user_input, allowed_range):
                    errors[column_name] = f"Input must be an integer within the range {allowed_range}."
            elif datatype == "float":
                allowed_range = column["standard_input_values"]["range"]
                if not self.validate_float_input(user_input, allowed_range):
                    errors[column_name] = f"Input must be a float within the range {allowed_range}."

            if column_name not in errors:
                user_inputs[column_name] = user_input    
        if errors:
            raise ValueError("Input validation errors", errors)    

        return user_inputs

    def prepare_queries(self, input_columns):
        query_for_ds2 = {}
        query_for_ds4 = {}
        for common_column in self.common_columns:
            standard_column_name = common_column["standard_column_name"]
            
            if standard_column_name in input_columns:
                df2_column_name = common_column["column"]["name"]["ds2"]
                if df2_column_name is not None:
                    query_for_ds2[df2_column_name] = input_columns[standard_column_name]
                
                df4_column_name = common_column["column"]["name"]["ds4"]
                if df4_column_name is not None:
                    query_for_ds4[df4_column_name] = input_columns[standard_column_name]

        return query_for_ds2, query_for_ds4
