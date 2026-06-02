import pandas as pd
import numpy as np


class DataCleaner:

    def __init__(

        self,

        df,

        schema

    ):

        self.df = df.copy()

        self.schema = schema

    def remove_duplicates(self):

        self.df = (
            self.df.drop_duplicates()
        )

    def remove_empty_columns(self):

        self.df = self.df.dropna(
            axis=1,
            how="all"
        )

    def clean_numeric_columns(self):

        for col, col_type in (

            self.schema.items()
        ):

            if col_type != "numeric":

                continue

            self.df[col] = (

                self.df[col]
                .astype(str)

                .str.replace(
                    r'[$₹€,£,%]',
                    '',
                    regex=True
                )

                .str.replace(
                    ',',
                    '',
                    regex=False
                )
            )

            self.df[col] = pd.to_numeric(

                self.df[col],

                errors="coerce"
            )

    def clean_date_columns(self):

        for col, col_type in (

            self.schema.items()
        ):

            if col_type != "date":

                continue

            self.df[col] = pd.to_datetime(

                self.df[col],

                errors="coerce"
            )

    def handle_missing_values(self):

        for col in self.df.columns:

            if pd.api.types.is_numeric_dtype(

                self.df[col]
            ):

                skew = (

                    self.df[col]
                    .skew()
                )

                if abs(skew) > 1:

                    fill_value = (

                        self.df[col]
                        .median()
                    )

                else:

                    fill_value = (

                        self.df[col]
                        .mean()
                    )

                self.df[col] = (

                    self.df[col]
                    .fillna(fill_value)
                )

            else:

                mode = (

                    self.df[col]
                    .mode()
                )

                if not mode.empty:

                    self.df[col] = (

                        self.df[col]
                        .fillna(mode[0])
                    )

    def clean_column_names(self):

        self.df.columns = (

            self.df.columns

            .astype(str)

            .str.strip()

            .str.replace(
                "\n",
                " "
            )
        )

    def clean(self):

        self.clean_column_names()

        self.remove_duplicates()

        self.remove_empty_columns()

        self.clean_numeric_columns()

        self.clean_date_columns()

        self.handle_missing_values()

        return self.df
