import plotly.express as px


class Visualizer:

    def __init__(self, df):

        self.df = df

    def histogram(self, column):

        return px.histogram(

            self.df,

            x=column,

            title=f"Distribution of {column}"
        )

    def scatter(self, x, y):

        return px.scatter(

            self.df,

            x=x,

            y=y,

            title=f"{x} vs {y}"
        )

    def bar(self, category, value):

        grouped = (

            self.df
            .groupby(category)[value]
            .mean()
            .reset_index()
        )

        return px.bar(

            grouped,

            x=category,

            y=value,

            title=f"{value} by {category}"
        )

    def line(self, date_col, value_col):

        grouped = (

            self.df
            .groupby(date_col)[value_col]
            .sum()
            .reset_index()
        )

        return px.line(

            grouped,

            x=date_col,

            y=value_col,

            title=f"{value_col} Trend"
        )

    def heatmap(self, corr_matrix):

        if corr_matrix is None:

            return None

        return px.imshow(

            corr_matrix,

            text_auto=True,

            title="Correlation Heatmap"
        )
