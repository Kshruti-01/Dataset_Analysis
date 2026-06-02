import plotly.express as px
import plotly.graph_objects as go


class Visualizer:

    def __init__(self, df):

        self.df = df

    # -------------------------
    # Histogram
    # -------------------------

    def histogram(self, column):

        return px.histogram(
            self.df,
            x=column,
            title=f"Distribution of {column}"
        )

    # -------------------------
    # Scatter Plot
    # -------------------------

    def scatter(self, x, y):

        return px.scatter(
            self.df,
            x=x,
            y=y,
            title=f"{x} vs {y}"
        )

    # -------------------------
    # Bar Chart
    # -------------------------

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

    # -------------------------
    # Line Chart
    # -------------------------

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

    # -------------------------
    # Box Plot
    # -------------------------

    def boxplot(self, column):

        return px.box(
            self.df,
            y=column,
            title=f"Outlier Analysis - {column}"
        )

    # -------------------------
    # Correlation Heatmap
    # -------------------------

    def heatmap(self, correlation_matrix):

        if correlation_matrix is None:
            return None

        return px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap"
        )
