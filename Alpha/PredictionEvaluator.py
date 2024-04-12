class PredictionEvaluator:
    def __init__(self):
        """
        Initialize the PredictionEvaluator with a dictionary to track class weights.
        """
        self.class_weights = []  # Stores cumulative weights for each class

    def add_prediction(self, prediction, weight=1):
        """
        Add a prediction to the class weights dictionary.
        :param prediction: List of dictionaries containing class and probability.
        :param weight: Weight to assign to the prediction.
        """
        # example prediction, could be more classes
        # [{'class': 0, 'probability': 0.9172860124950649}, {'class': 1, 'probability': 0.08271398750493499}]
        
        # for each class in the prediction, add a property weighted_prob
        model = []
        for pred in prediction:
            cls = pred['class']
            prob = pred['probability']
            weighted_prob = prob * weight
            model.append({'class': cls, 'probability': prob, 'weighted_prob': weighted_prob})
        self.class_weights.append(model)

    def get_best_class(self):
        """
        Determine the class with the highest cumulative weighted probability.
        :return: Tuple containing the class index and its weighted sum.
        """
        if not self.class_weights:
            return None, None  # No data has been added

        # for each class, sum the weighted probabilities
        class_sums = {}
        for model in self.class_weights:
            for pred in model:
                cls = pred['class']
                weighted_prob = pred['weighted_prob']
                class_sums[cls] = class_sums.get(cls, 0) + weighted_prob
        
        # find the class with the highest sum
        best_class = max(class_sums, key=class_sums.get)
        max_weight = class_sums[best_class]
        return best_class, max_weight

    def __str__(self):
        best_class, max_weight = self.get_best_class()
        return f"Class {best_class} has the highest cumulative weighted probability of {max_weight:.4f}"
