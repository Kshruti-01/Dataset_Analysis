class InsightGenerator:

    def __init__(

        self,

        df,

        schema,

        relationships

    ):

        self.df = df

        self.schema = schema

        self.relationships = relationships

    def generate(self):

        insights = []

        numeric_cols = [

            c

            for c, t

            in self.schema.items()

            if t == "numeric"
        ]

        for col in numeric_cols:

            avg = round(

                self.df[col].mean(),

                2
            )

            insights.append(

                f"Average {col} is {avg}"
            )

            insights.append(

                f"Maximum {col} is {self.df[col].max()}"
            )

        for rel in self.relationships:

            insights.append(

                f"{rel['column_1']} and "
                f"{rel['column_2']} have "
                f"a correlation of "
                f"{rel['correlation']}"
            )

        return insights
