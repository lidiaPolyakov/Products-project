import unittest
import pandas as pd
import numpy as np
import json
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))

from knn_data_processor import KNNDataProcessor

class TestKNNDataProcessor(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        with open(sys.path[0] + '/test_common_columns.json') as f:
            self.common_columns = json.load(f)
        self.df = pd.DataFrame({
            "color": ["red", "blue", "blue", "red"],
            "height": [1.5, 1.8, 1.6, 1.7]
        })
        self.df["color"] = self.df["color"].astype("category")
        self.df.name = "df1"

        self.user_input = { "color": "red", "height": 1.55 }

        self.processor = KNNDataProcessor(self.common_columns, self.df, self.user_input)

    def test_initialization(self):
        self.assertIsNotNone(self.processor.df_copy)
        self.assertEqual(self.processor.df_copy.name, "df1")
        self.assertTrue("color" in self.processor.label_encoders)
        self.assertTrue("height" in self.processor.scalers)

    def test_nearest_neighbor_metric(self):
        x = np.array([0, 1.55])
        y = np.array([1, 1.70])
        
        # turn x and y second element into scaled values
        x[1] = self.processor.scalers["height"].transform( pd.DataFrame({ "height": [x[1]] }) )[0, 0]
        y[1] = self.processor.scalers["height"].transform( pd.DataFrame({ "height": [x[1]] }) )[0, 0]
        
        distance = self.processor.nearest_neighbor_metric(x, y)
        self.assertAlmostEqual(distance, 1.11803, places=5)

    def test_find_nearest_neighbor(self):
        nearest_neighbor = self.processor.find_nearest_neighbor(n_neighbors=2)
        self.assertEqual(nearest_neighbor["color"], "red")
        self.assertAlmostEqual(nearest_neighbor["height"], 1.55, places=2)

if __name__ == '__main__':
    unittest.main()
