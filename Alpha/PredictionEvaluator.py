class PredictionEvaluator:
    def __init__(self):
        """
        Initialize the PredictionEvaluator with a dictionary to track class weights.
        """
        self.total_weights = {0: 0, 1: 0}  # Tracks total weights for each class (0 and 1)

    def add_prediction(self, prediction, evaluation):
        """
        Add a prediction to the evaluator.
        :param prediction: The predicted class (assumed to be the most likely class).
        :param evaluation: The evaluation result including accuracy.
        """
        # Extract the model's accuracy as the weight
        weight = evaluation['accuracy']

        # Update the total weight for the predicted class
        self.total_weights[prediction] += weight

    def evaluate_risk_assessment(self):
        """
        Evaluate the risk assessment based on the evaluation results.
        Class 0: Not risky
        Class 1: Risky
        return: classes of risk assessment (low, medium, high)
        """
        total_0 = self.total_weights[0]
        total_1 = self.total_weights[1]
        
        if total_1 > total_0:
            if total_1 / (total_0 + total_1) > 0.5:  # More than 50% of the weight is towards class 1
                return "high"
            else:
                return "medium"
        else:
            if total_0 / (total_0 + total_1) > 0.5:  # More than 50% of the weight is towards class 0
                return "low"
            else:
                return "medium"
