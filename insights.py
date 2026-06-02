class InsightGenerator:

    def __init__(

        self,

        df,

        schema,

        analysis_results,

        relationships

    ):

        self.df = df

        self.schema = schema

        self.analysis_results = analysis_results

        self.relationships = relationships

    def generate(self):

        insights = []

        # Dataset Summary

        summary = self.analysis_results.get(
            "Dataset Summary",
            {}
        )

        insights.append(

            f"The dataset contains "
            f"{summary.get('Rows',0)} rows and "
            f"{summary.get('Columns',0)} columns."
        )

        # Numeric Insights

        numeric = self.analysis_results.get(
            "Numeric Analysis",
            {}
        )

        for col, stats in numeric.items():

            insights.append(

                f"The average value of "
                f"{col} is "
                f"{stats['Mean']}."
            )

            insights.append(

                f"The maximum value recorded "
                f"in {col} is "
                f"{stats['Max']}."
            )

        # Outliers

        outliers = self.analysis_results.get(
            "Outlier Analysis",
            {}
        )

        for col, count in outliers.items():

            if count > 0:

                insights.append(

                    f"{count} potential "
                    f"outliers detected in "
                    f"{col}."
                )

        # Relationships

        for rel in self.relationships:

            insights.append(

                f"{rel['Column1']} and "
                f"{rel['Column2']} show a "
                f"strong correlation of "
                f"{rel['Correlation']}."
            )

        if not insights:

            insights.append(
                "No major insights detected."
            )

        return insights
