import pandas as pd


class RelationshipEngine:

    def __init__(

        self,

        df,

        schema

    ):

        self.df = df

        self.schema = schema

    def get_numeric_columns(self):

        return [

            col

            for col, dtype

            in self.schema.items()

            if dtype == "numeric"
        ]

    def correlation_matrix(self):

        numeric_cols = (

            self.get_numeric_columns()
        )

        if len(numeric_cols) < 2:

            return None

        return (

            self.df[numeric_cols]
            .corr()
        )

    def strong_relationships(

        self,

        threshold=0.7

    ):

        corr = (

            self.correlation_matrix()
        )

        if corr is None:

            return []

        relationships = []

        for col1 in corr.columns:

            for col2 in corr.columns:

                if col1 >= col2:

                    continue

                value = corr.loc[
                    col1,
                    col2
                ]

                if abs(value) >= threshold:

                    relationships.append({

                        "Column1": col1,

                        "Column2": col2,

                        "Correlation":
                        round(value, 2)
                    })

        return relationships
