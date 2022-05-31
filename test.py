
import unittest

import pandas as pd

from transformer import Transformer


class TestTransformer(unittest.TestCase):
    def setUp(self):
        self.transformations = {
            "mid": {
                "operation": "divide",
                "columns": {
                    "numerator": "sum_high_low",
                    "denominator": 2.0,
                },
                "steps": {
                    "sum_high_low": {
                        "operation": "sum",
                        "columns": ["High", "Low"]
                    }
                }
            }
        }
        self.renames = {
            "High": "high",
            "Low": "low",
            "Date": "date",
        }
        self.output_fields = ["date", "high", "low", "mid"]
        self.test_transformer_data = [
            {
                "High": 3,
                "Low": 1,
                "Date": "2022-12-04",
                "ToBeDropped": 123,

            },
        ]
        self.test_transformer_output = [
            {
                "high": 3,
                "low": 1,
                "mid": 2,
                "date": "2022-12-04",
            },
        ]

    def test_transformer(self):
        transformer = Transformer()
        df = pd.DataFrame(self.test_transformer_data)
        transformer(df, self.transformations, self.renames, self.output_fields)

        result_list = transformer.transformed_df_as_dicts
        result_item = result_list[0]

        # result set level assertions
        assert len(result_list) == len(self.test_transformer_output)

        # item level assertions
        # are the output fields correct?
        expected_item = self.test_transformer_output[0]
        result_fields = sorted(expected_item.keys())
        expected_fields = sorted(result_item.keys())
        assert result_fields == expected_fields
        # are the field values correct?
        for result_field, expected_field in zip(result_fields, expected_fields):
            assert result_item[result_field] == expected_item[expected_field]
