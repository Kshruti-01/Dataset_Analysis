import pandas as pd
import numpy as np


class SchemaDetector:

    def __init__(self, df):

        self.df = df

    def classify_column(self, column):

        series = self.df[column]

        series = series.dropna()

        if len(series) == 0:

            return "unknown"

        string_series = series.astype(str)

        total_rows = len(series)

        unique_count = series.nunique()

        unique_ratio = (
            unique_count / total_rows
        )

        # Boolean

        unique_values = {

            str(v).strip().lower()

            for v in string_series.unique()
        }

        boolean_values = {

            "true",
            "false",
            "yes",
            "no",
            "0",
            "1"
        }

        if unique_values.issubset(
            boolean_values
        ):

            return "boolean"

        # Numeric

        numeric_series = pd.to_numeric(

            string_series
            .str.replace(
                r'[$₹€,£,%]',
                '',
                regex=True
            )
            .str.replace(
                ',',
                '',
                regex=False
            ),

            errors="coerce"
        )

        numeric_ratio = (

            numeric_series.notna()
            .sum()

            /

            total_rows
        )

        if numeric_ratio > 0.9:

            if unique_ratio > 0.98:

                return "identifier"

            return "numeric"

        # Date

        date_series = pd.to_datetime(

            series,

            errors="coerce"
        )

        date_ratio = (

            date_series.notna()
            .sum()

            /

            total_rows
        )

        if date_ratio > 0.9:

            return "date"

        # Categorical

        if unique_ratio < 0.3:

            return "categorical"

        avg_len = (

            string_series
            .str.len()
            .mean()
        )

        if avg_len > 30:

            return "text"

        return "categorical"

    def detect_schema(self):

        schema = {}

        for col in self.df.columns:

            schema[col] = (

                self.classify_column(col)
            )

        return schema
