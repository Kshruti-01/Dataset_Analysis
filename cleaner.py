import pandas as pd
import numpy as np

class DataCleaner:
    @staticmethod
    def clean_dataset(df):
        # Remove duplicate rows
        df = df.drop_duplicates()
        # Remove extra spaces from column names
        df.columns = df.columns.astype(str).str.strip()
        # Remove fully empty columns
        df = df.dropna(axis=1, how='all')

        # ---------------- NUMERIC COLUMNS ---------------- #

        numeric_cols = df.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].mean())

        # ---------------- CATEGORICAL COLUMNS ---------------- #

        categorical_cols = df.select_dtypes(include='object').columns
        for col in categorical_cols:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])
        return df
