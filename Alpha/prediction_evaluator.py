class PredictionEvaluator:
    def __init__(self):
        """
        Initialize the PredictionEvaluator with a dictionary to track class weights.
        """
        self.models_accuracies = { 0: [], 1: [] }

    def add_prediction(self, prediction, evaluation):
        """
        Add a prediction to the evaluator.
        :param prediction: The predicted class (assumed to be the most likely class).
        :param evaluation: The evaluation result including accuracy.
        """
        self.models_accuracies[prediction].append(evaluation['accuracy'])

    def evaluate_risk_assessment(self):
        """
        Evaluate the risk assessment based on the evaluation results.
        Class 0: Not risky
        Class 1: Risky
        return: classes of risk assessment (low, medium, high)
        """
        
        model_accuracies_0 = sum(self.models_accuracies[0])
        model_accuracies_1 = sum(self.models_accuracies[1])
        avg_model_accuracies_cls_0 = model_accuracies_0 / (model_accuracies_0 + model_accuracies_1)
        avg_model_accuracies_cls_1 = model_accuracies_1 / (model_accuracies_0 + model_accuracies_1)
        
        if model_accuracies_1 > model_accuracies_0:
            if avg_model_accuracies_cls_1 > 0.5:  # More than 50% of the weight is towards class 1
                return "high"
            else:
                return "medium"
        else:
            if avg_model_accuracies_cls_0 > 0.5:  # More than 50% of the weight is towards class 0
                return "low"
            else:
                return "medium"
