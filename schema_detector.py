import pandas as pd
import re


class SchemaDetector:

    def __init__(self, df):

        self.df = df

    def classify_column(self, column):

        series = self.df[column]

        col_name = str(column).lower()

        # ID detection

        if (
            "id" in col_name
            or "code" in col_name
        ):

            return "identifier"

        # Date detection

        try:

            converted = pd.to_datetime(
                series,
                errors="coerce"
            )

            if converted.notna().mean() > 0.8:

                return "date"

        except:

            pass

        # Numeric

        numeric = pd.to_numeric(
            series,
            errors="coerce"
        )

        if numeric.notna().mean() > 0.8:

            return "numeric"

        # Low cardinality

        unique_ratio = (
            series.nunique()
            / len(series)
        )

        if unique_ratio < 0.2:

            return "categorical"

        return "text"

    def detect_schema(self):

        schema = {}

        for col in self.df.columns:

            schema[col] = self.classify_column(
                col
            )

        return schema
