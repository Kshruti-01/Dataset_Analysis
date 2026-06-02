class RecommendationEngine:

    def __init__(self, df, schema):

        self.df = df
        self.schema = schema

    def recommend_visualizations(self):

        recommendations = []

        numeric_cols = [

            c

            for c, t

            in self.schema.items()

            if t == "numeric"
        ]

        categorical_cols = [

            c

            for c, t

            in self.schema.items()

            if t == "categorical"
        ]

        date_cols = [

            c

            for c, t

            in self.schema.items()

            if t == "date"
        ]

        # Histogram

        for col in numeric_cols:

            recommendations.append({

                "type": "histogram",
                "column": col
            })

        # Scatter

        if len(numeric_cols) >= 2:

            for i in range(

                len(numeric_cols) - 1
            ):

                recommendations.append({

                    "type": "scatter",

                    "x": numeric_cols[i],

                    "y": numeric_cols[i + 1]
                })

        # Bar

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
