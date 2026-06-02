import pandas as pd
import numpy as np


class RelationshipEngine:

    def __init__(self, df, schema):

        self.df = df
        self.schema = schema

    def get_numeric_columns(self):

        return [

            col

            for col, col_type

            in self.schema.items()

            if col_type == "numeric"
        ]

    def correlation_analysis(self):

        numeric_cols = self.get_numeric_columns()

        if len(numeric_cols) < 2:

            return None

        return (

            self.df[numeric_cols]
            .corr(method='pearson')
        )

    def strong_relationships(self):

        corr_matrix = self.correlation_analysis()

        if corr_matrix is None:

            return []

        relationships = []

        for col1 in corr_matrix.columns:

            for col2 in corr_matrix.columns:

                if col1 >= col2:

                    continue

                corr = corr_matrix.loc[
                    col1,
                    col2
                ]

                if abs(corr) >= 0.7:

                    relationships.append({

                        "column_1": col1,
                        "column_2": col2,
                        "correlation": round(
                            corr,
                            2
                        )
                    })

        return relationships
