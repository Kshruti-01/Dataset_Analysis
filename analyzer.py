import pandas as pd
import numpy as np

class DatasetAnalyzer:
    def __init__(self, df):
        self.df = df

    # ---------------- DATASET INFO ---------------- #
    def dataset_info(self):
        info = {
            "Rows": self.df.shape[0],
            "Columns": self.df.shape[1],
            "Column Names": list(self.df.columns),
            "Missing Values": self.df.isnull().sum().to_dict(),
            "Data Types": self.df.dtypes.astype(str).to_dict()
        }
        return info
    # ---------------- NUMERIC COLUMNS ---------------- #
    def numerical_columns(self):
        return list(
            self.df.select_dtypes(include=np.number).columns
        )
    # ---------------- CATEGORICAL COLUMNS ---------------- #
    def categorical_columns(self):
        return list(
            self.df.select_dtypes(include='object').columns
        )
    # ---------------- NUMERICAL ANALYSIS ---------------- #
    def numerical_analysis(self):
        numeric_df = self.df.select_dtypes(include=np.number)

        # Prevent crash
        if numeric_df.empty:
            return "No numerical columns found in dataset."
        return numeric_df.describe().T

    # ---------------- CATEGORICAL ANALYSIS ---------------- #
    def categorical_analysis(self):
        categorical_cols = self.categorical_columns()
        # Prevent crash
        if len(categorical_cols) == 0:
            return "No categorical columns found."
        summary = {}
        for col in categorical_cols:
            summary[col] = (self.df[col].value_counts().head(10).to_dict())
        return summary

    # ---------------- CORRELATION ---------------- #
    def correlation_matrix(self):
        numeric_df = self.df.select_dtypes(include=np.number)
        if numeric_df.empty:
            return None
        return numeric_df.corr()

    # ---------------- DATE DETECTION ---------------- #
    def detect_date_columns(self):
        date_cols = []
        for col in self.df.columns:
            try:
                pd.to_datetime(self.df[col])
                date_cols.append(col)
            except:
                pass
        return date_cols
