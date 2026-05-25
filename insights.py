import numpy as np

class InsightGenerator:
    def __init__(self, df):
        self.df = df

    def generate_insights(self):
        insights = []
        numeric_cols = (self.df.select_dtypes(include=np.number).columns)

        # ---------------- BASIC STATS ---------------- #
        for col in numeric_cols:
            try:
                avg = round(self.df[col].mean(),2)
                max_value = self.df[col].max()
                min_value = self.df[col].min()

                insights.append(f"Average {col} is {avg}")
                insights.append(f"Highest {col} is {max_value}")
                insights.append(f"Lowest {col} is {min_value}")

            except:
                pass
        # ---------------- CORRELATION INSIGHTS ---------------- #
        if len(numeric_cols) >= 2:
            corr_matrix = (self.df[numeric_cols].corr())
            for col1 in corr_matrix.columns:
                for col2 in corr_matrix.columns:
                    if col1 != col2:
                        corr = corr_matrix.loc[col1,col2]
                        if corr > 0.75:
                            insights.append(f"Strong positive relationship between {col1} and {col2}")
                        elif corr < -0.75:
                            insights.append(f"Strong negative relationship between {col1} and {col2}")
        return list(set(insights))
