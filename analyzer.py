import pandas as pd
import numpy as np


class DataAnalyzer:

    def __init__(self, df, schema):

        self.df = df
        self.schema = schema

    def dataset_summary(self):

        return {

            "Rows": len(self.df),

            "Columns": len(self.df.columns),

            "Missing Values":
            int(self.df.isnull().sum().sum()),

            "Duplicate Rows":
            int(self.df.duplicated().sum())
        }

    def numeric_analysis(self):

        results = {}

        numeric_cols = [

            col

            for col, dtype

            in self.schema.items()

            if dtype == "numeric"
        ]

        for col in numeric_cols:

            try:

                results[col] = {

                    "Mean":
                    round(
                        self.df[col].mean(),
                        2
                    ),

                    "Median":
                    round(
                        self.df[col].median(),
                        2
                    ),

                    "Min":
                    round(
                        self.df[col].min(),
                        2
                    ),

                    "Max":
                    round(
                        self.df[col].max(),
                        2
                    ),

                    "Std":
                    round(
                        self.df[col].std(),
                        2
                    ),

                    "Missing":
                    int(
                        self.df[col]
                        .isnull()
                        .sum()
                    )
                }

            except:

                continue

        return results

    def categorical_analysis(self):

        results = {}

        categorical_cols = [

            col

            for col, dtype

            in self.schema.items()

            if dtype == "categorical"
        ]

        for col in categorical_cols:

            try:

                mode = self.df[col].mode()

                results[col] = {

                    "Unique Values":
                    int(
                        self.df[col]
                        .nunique()
                    ),

                    "Top Category":
                    mode.iloc[0]
                    if not mode.empty
                    else None
                }

            except:

                continue

        return results

    def date_analysis(self):

        results = {}

        date_cols = [

            col

            for col, dtype

            in self.schema.items()

            if dtype == "date"
        ]

        for col in date_cols:

            try:

                results[col] = {

                    "Start":
                    str(
                        self.df[col].min()
                    ),

                    "End":
                    str(
                        self.df[col].max()
                    )
                }

            except:

                continue

        return results

    def outlier_analysis(self):

        outliers = {}

        numeric_cols = [

            col

            for col, dtype

            in self.schema.items()

            if dtype == "numeric"
        ]

        for col in numeric_cols:

            try:

                q1 = self.df[col].quantile(0.25)

                q3 = self.df[col].quantile(0.75)

                iqr = q3 - q1

                lower = q1 - 1.5 * iqr

                upper = q3 + 1.5 * iqr

                count = len(

                    self.df[

                        (self.df[col] < lower)

                        |

                        (self.df[col] > upper)

                    ]
                )

                outliers[col] = count

            except:

                continue

        return outliers

    def run_analysis(self):

        return {

            "Dataset Summary":
            self.dataset_summary(),

            "Numeric Analysis":
            self.numeric_analysis(),

            "Categorical Analysis":
            self.categorical_analysis(),

            "Date Analysis":
            self.date_analysis(),

            "Outlier Analysis":
            self.outlier_analysis()
        }
