import pandas as pd
import numpy as np


class DataAnalyzer:

    def __init__(self, df, schema):

        self.df = df
        self.schema = schema

    # ---------------------------
    # Column Groups
    # ---------------------------

    def get_numeric_columns(self):

        return [

            col

            for col, col_type

            in self.schema.items()

            if col_type == "numeric"
        ]

    def get_categorical_columns(self):

        return [

            col

            for col, col_type

            in self.schema.items()

            if col_type == "categorical"
        ]

    def get_date_columns(self):

        return [

            col

            for col, col_type

            in self.schema.items()

            if col_type == "date"
        ]

    # ---------------------------
    # Dataset Summary
    # ---------------------------

    def dataset_summary(self):

        return {

            "rows": len(self.df),

            "columns": len(self.df.columns),

            "missing_values": int(
                self.df.isnull().sum().sum()
            ),

            "duplicates": int(
                self.df.duplicated().sum()
            )
        }

    # ---------------------------
    # Numeric Analysis
    # ---------------------------

    def numeric_analysis(self):

        numeric_cols = self.get_numeric_columns()

        if not numeric_cols:

            return {}

        results = {}

        for col in numeric_cols:

            try:

                results[col] = {

                    "mean": round(
                        self.df[col].mean(),
                        2
                    ),

                    "median": round(
                        self.df[col].median(),
                        2
                    ),

                    "minimum": round(
                        self.df[col].min(),
                        2
                    ),

                    "maximum": round(
                        self.df[col].max(),
                        2
                    ),

                    "std_dev": round(
                        self.df[col].std(),
                        2
                    ),

                    "variance": round(
                        self.df[col].var(),
                        2
                    ),

                    "skewness": round(
                        self.df[col].skew(),
                        2
                    )
                }

            except Exception:

                continue

        return results

    # ---------------------------
    # Categorical Analysis
    # ---------------------------

    def categorical_analysis(self):

        categorical_cols = (
            self.get_categorical_columns()
        )

        results = {}

        for col in categorical_cols:

            try:

                results[col] = {

                    "unique_values": int(
                        self.df[col].nunique()
                    ),

                    "top_category":
                    self.df[col]
                    .mode()[0]

                    if not self.df[col]
                    .mode()
                    .empty

                    else None,

                    "top_frequency":

                    int(

                        self.df[col]
                        .value_counts()
                        .iloc[0]

                    )

                    if not self.df[col]
                    .value_counts()
                    .empty

                    else 0
                }

            except Exception:

                continue

        return results

    # ---------------------------
    # Date Analysis
    # ---------------------------

    def date_analysis(self):

        date_cols = self.get_date_columns()

        results = {}

        for col in date_cols:

            try:

                results[col] = {

                    "start_date":

                    str(
                        self.df[col].min()
                    ),

                    "end_date":

                    str(
                        self.df[col].max()
                    ),

                    "total_days":

                    int(

                        (
                            self.df[col].max()

                            -

                            self.df[col].min()

                        ).days
                    )
                }

            except Exception:

                continue

        return results

    # ---------------------------
    # Outlier Detection
    # ---------------------------

    def detect_outliers(self):

        numeric_cols = (
            self.get_numeric_columns()
        )

        outlier_report = {}

        for col in numeric_cols:

            try:

                q1 = (
                    self.df[col]
                    .quantile(0.25)
                )

                q3 = (
                    self.df[col]
                    .quantile(0.75)
                )

                iqr = q3 - q1

                lower = q1 - 1.5 * iqr

                upper = q3 + 1.5 * iqr

                outliers = self.df[

                    (self.df[col] < lower)

                    |

                    (self.df[col] > upper)

                ]

                outlier_report[col] = {

                    "outlier_count":
                    len(outliers),

                    "percentage":
                    round(

                        len(outliers)

                        /

                        len(self.df)

                        * 100,

                        2

                    )
                }

            except Exception:

                continue

        return outlier_report

    # ---------------------------
    # Full Analysis
    # ---------------------------

    def run_complete_analysis(self):

        return {

            "dataset_summary":
            self.dataset_summary(),

            "numeric_analysis":
            self.numeric_analysis(),

            "categorical_analysis":
            self.categorical_analysis(),

            "date_analysis":
            self.date_analysis(),

            "outliers":
            self.detect_outliers()
        }
