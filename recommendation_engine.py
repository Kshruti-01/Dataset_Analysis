class RecommendationEngine:

    def __init__(

        self,

        df,

        schema

    ):

        self.df = df

        self.schema = schema

    def recommend(self):

        recommendations = []

        numeric_cols = [

            col

            for col, dtype

            in self.schema.items()

            if dtype == "numeric"
        ]

        categorical_cols = [

            col

            for col, dtype

            in self.schema.items()

            if dtype == "categorical"
        ]

        date_cols = [

            col

            for col, dtype

            in self.schema.items()

            if dtype == "date"
        ]

        # Histograms

        for col in numeric_cols:

            recommendations.append({

                "type": "histogram",

                "column": col
            })

        # Scatter

        for i in range(

            len(numeric_cols)
        ):

            for j in range(

                i + 1,

                len(numeric_cols)
            ):

                recommendations.append({

                    "type": "scatter",

                    "x": numeric_cols[i],

                    "y": numeric_cols[j]
                })

        # Bar Charts

        for cat in categorical_cols:

            for num in numeric_cols:

                recommendations.append({

                    "type": "bar",

                    "category": cat,

                    "value": num
                })

        # Time Series

        for date_col in date_cols:

            for num_col in numeric_cols:

                recommendations.append({

                    "type": "line",

                    "date": date_col,

                    "value": num_col
                })

        return recommendations
