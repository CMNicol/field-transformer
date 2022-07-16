import typing

import pandas as pd


class Transformer:

    def __init__(self):
        self.OPERATIONS = {"divide": self.divide, "sum": self.summer}

    def divide(self, row: pd.Series, columns: typing.Dict):
        denominator_is_a_column = isinstance(columns["denominator"], str)
        numerator = row[columns["numerator"]]
        denominator = row[columns["denominator"]
                          ] if denominator_is_a_column else columns["denominator"]
        return numerator/denominator

    def summer(self, row: pd.Series, columns: typing.Dict):
        a = row[columns[0]]
        b = row[columns[-1]]
        return a+b

    def row_operation(self, row: pd.Series, calc: typing.Dict):
        """
        Contains the logic to interpret and apply the operations defined in `calc` to the `row`.

        This is a recursive method.
        """
        steps = calc.get("steps")
        if steps:
            for step_name, step_calc in steps.items():
                row[step_name] = self.row_operation(row, step_calc)

        operation = self.OPERATIONS[calc["operation"]]
        columns = calc["columns"]
        return operation(row, columns)

    def make_new_columns(self, dataframe: pd.DataFrame, transformations: typing.Dict):
        """
        Loops through each transformation which results in a new column.
        """
        for new_column, calc_object in transformations.items():
            dataframe[new_column] = dataframe.apply(
                lambda row: self.row_operation(row, calc_object), axis=1)

    def rename_columns(self, df: pd.DataFrame, renames: typing.Dict):
        """Renames the columns of the dataframe in-place."""
        df.rename(columns=renames, inplace=True)

    def format_to_output_structure(self, df: pd.DataFrame, structure: typing.List):
        self.more_info = df[df.columns.difference(
            list(structure)+["_id"])].to_dict(orient="records")
        df.drop(columns=df.columns.difference(structure), inplace=True)

    def __call__(self, df: pd.DataFrame, transformations: typing.Dict, renames: typing.Dict, structure: typing.Dict):
        """Pass in a copy of the df if you want to preserve the original."""
        if transformations:
            self.make_new_columns(df, transformations)
        if renames:
            self.rename_columns(df, renames)
        if structure:
            self.format_to_output_structure(df, structure)

        self.transformed_df = df
        self.transformed_df_as_dicts = df.to_dict(orient="records")

    def add_more_info_field(self):
        for record, info in zip(self.transformed_df_as_dicts, self.more_info):
            record.update({"more_info": info})
