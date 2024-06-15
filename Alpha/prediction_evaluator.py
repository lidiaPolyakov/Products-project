class PredictionEvaluator:
    def __init__(self, ds2, ds4):
        """
        Initialize the PredictionEvaluator with a dictionary to track class weights.
        """
        self.__models_for_ds2 = []
        self.__models_for_ds4 = []

        self.__doctor_votes_ds2 = ds2["doctor_votes"]
        self.__doctor_votes_ds4 = ds4["doctor_votes"]
        
        self.__num_rows_ds2 = ds2["num_rows"]
        self.__num_rows_ds4 = ds4["num_rows"]
        
        if (self.__doctor_votes_ds2, self.__doctor_votes_ds4) == (0, 0):
            raise ValueError("Both ds2_weight and ds4_weight cannot be zero")

    def add_prediction(self, prediction, evaluation, ds_name):
        """
        Add a prediction to the evaluator.
        :param prediction: The predicted class (assumed to be the most likely class).
        :param evaluation: The evaluation result including accuracy.
        """
        def arr(ds_name):
            if ds_name == 'ds2':
                return self.__models_for_ds2
            elif ds_name == 'ds4':
                return self.__models_for_ds4
            else:
                raise ValueError("Invalid ds_name. Must be either 'ds2' or 'ds4'")

        arr(ds_name).append({
            "prediction": prediction,
            "accuracy": evaluation['accuracy'],
            "name": evaluation['name']
        })

    def evaluate_risk_assessment(self):
        """
        Evaluate the risk assessment based on the evaluation results.
        Class 0: Not risky
        Class 1: Risky
        return: classes of risk assessment (low, medium, high)
        """

        num_rows_ds2 = self.__num_rows_ds2
        num_rows_ds4 = self.__num_rows_ds4
        
        doctor_votes_ds2 = self.__doctor_votes_ds2
        doctor_votes_ds4 = self.__doctor_votes_ds4
        
        weight_num_rows_ds2 = num_rows_ds2 / (num_rows_ds2 + num_rows_ds4)
        weight_num_rows_ds4 = num_rows_ds4 / (num_rows_ds2 + num_rows_ds4)
        
        weight_doctor_votes_ds2 = doctor_votes_ds2 / (doctor_votes_ds2 + doctor_votes_ds4)
        weight_doctor_votes_ds4 = doctor_votes_ds4 / (doctor_votes_ds2 + doctor_votes_ds4)
        
        ds2 = 0
        if len(self.__models_for_ds2) != 0:
            for model in self.__models_for_ds2:
                ds2 += model['prediction'] * model['accuracy']
            ds2 /= len(self.__models_for_ds2)
            ds2 *= (weight_doctor_votes_ds2 + weight_num_rows_ds2) / 2
        
        ds4 = 0
        if len(self.__models_for_ds4) != 0:
            for model in self.__models_for_ds4:
                ds4 += model['prediction'] * model['accuracy']
            ds4 /= len(self.__models_for_ds4)
            ds4 *= (weight_doctor_votes_ds4 + weight_num_rows_ds4) / 2
        
        risk_precentage = ds2 + ds4
        models = self.__models_for_ds2 + self.__models_for_ds4
        
        if (2/3) < risk_precentage <= 1:
            return "high", risk_precentage, models
        
        if (1/3) <= risk_precentage <= (2/3):
            return "medium", risk_precentage, models
        
        return "low", risk_precentage, models

