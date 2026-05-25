import plotly.express as px
import plotly.graph_objects as go
import numpy as np

class Visualizer:
    def __init__(self, df):
        self.df = df

    # ---------------- HISTOGRAM ---------------- #
    def histogram(self, column):
        fig = px.histogram(self.df,x=column,nbins=20,title=f"Distribution of {column}")
        return fig

    # ---------------- SCATTER PLOT ---------------- #
    def scatter_plot(self, x_col, y_col):
        fig = px.scatter(self.df,x=x_col,y=y_col,title=f"{x_col} vs {y_col}")
        return fig

    # ---------------- BAR CHART ---------------- #
    def bar_chart(self, category_col, numeric_col):
        grouped = (self.df.groupby(category_col)[numeric_col].mean().reset_index())
        fig = px.bar(grouped,x=category_col,y=numeric_col,title=f"{numeric_col} by {category_col}")
        return fig

    # ---------------- HEATMAP ---------------- #
    def correlation_heatmap(self):
        numeric_df = self.df.select_dtypes(include=np.number)
        # Prevent crash
        if numeric_df.empty:
            return None
        corr = numeric_df.corr()
        fig = px.imshow(corr,text_auto=True,aspect="auto",title="Correlation Heatmap")
        return fig

    # ---------------- AUTO GRAPH GENERATION ---------------- #
    def generate_automatic_graphs(self):
        graphs = []
        numeric_cols = list(self.df.select_dtypes(include=np.number).columns)
        categorical_cols = list(self.df.select_dtypes(include='object').columns)
        MAX_GRAPHS = 10

        # ---------------- HISTOGRAMS ---------------- #
        for col in numeric_cols[:3]:
            if len(graphs) >= MAX_GRAPHS:
                return graphs
            try:
                graphs.append(self.histogram(col))
            except:
                pass

        # ---------------- SCATTER PLOTS ---------------- #
        if len(numeric_cols) >= 2:
            for i in range(min(len(numeric_cols)-1, 3)):
                if len(graphs) >= MAX_GRAPHS:
                    return graphs
                try:
                    graphs.append(

                        self.scatter_plot(numeric_cols[i],numeric_cols[i + 1]))
                except:
                    pass

        # ---------------- BAR CHARTS ---------------- #
        for cat_col in categorical_cols[:2]:
            for num_col in numeric_cols[:2]:
                if len(graphs) >= MAX_GRAPHS:
                    return graphs
                try:
                    graphs.append(
                        self.bar_chart(cat_col,num_col))
                except:
                    pass
        return graphs
