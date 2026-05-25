import streamlit as st
import pandas as pd

from analysis.loader import DatasetLoader
from analysis.cleaner import DataCleaner
from analysis.analyzer import DatasetAnalyzer
from analysis.visualizer import Visualizer
from analysis.insights import InsightGenerator


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Smart Dataset Analyzer",
    layout="wide")

# ---------------- TITLE ---------------- #
st.title("Dataset Analysis & Visualization System")
st.markdown(
    """
Upload a dataset and the system will:
- Understand dataset structure
- Analyze columns
- Generate statistics
- Compare relationships
- Create graphs automatically
- Generate insights
"""
)
# ---------------- FILE UPLOAD ---------------- #
uploaded_file = st.file_uploader("Upload CSV or Excel File",type=["csv", "xlsx"])

# ---------------- PROCESS DATASET ---------------- #
if uploaded_file is not None:
    try:
        # Load dataset
        df = DatasetLoader.load_file(uploaded_file)
        # Clean dataset
        df = DataCleaner.clean_dataset(df)
        # Check if dataframe empty
        if df.empty:
            st.error("Uploaded dataset is empty.")
            st.stop()

        # Create objects
        analyzer = DatasetAnalyzer(df)
        visualizer = Visualizer(df)
        insight_generator = InsightGenerator(df)

        # ---------------- DATASET PREVIEW ---------------- #
        st.header("Dataset Preview")
        st.dataframe(df,use_container_width=True)

        # ---------------- DATASET STRUCTURE ---------------- #
        st.header("Dataset Structure")
        info = analyzer.dataset_info()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows",info["Rows"])
        with col2:
            st.metric("Columns",info["Columns"])
        st.subheader("Column Names")
        st.write(info["Column Names"])
        st.subheader("Data Types")
        st.json(info["Data Types"])
        st.subheader("Missing Values")
        st.json(info["Missing Values"])

        # ---------------- NUMERICAL ANALYSIS ---------------- #
        st.header("Numerical Analysis")
        numerical_result = (analyzer.numerical_analysis())
        if isinstance(numerical_result,str):
            st.warning(numerical_result)
        else:
            st.dataframe(numerical_result,use_container_width=True)

        # ---------------- CATEGORICAL ANALYSIS ---------------- #
        st.header("Categorical Analysis")
        categorical_result = (analyzer.categorical_analysis())
        if isinstance(categorical_result,str):
            st.warning(categorical_result)
        else:
            for col, values in categorical_result.items():
                st.subheader(col)
                st.write(values)

        # ---------------- INSIGHTS ---------------- #
        st.header("Generated Insights")
        insights = (insight_generator.generate_insights())
        if len(insights) == 0:
            st.warning("No insights generated.")
        else:
            for insight in insights:
                st.success(insight)

        # ---------------- HEATMAP ---------------- #
        st.header("Correlation Heatmap")
        heatmap = (visualizer.correlation_heatmap())
        if heatmap is not None:
            st.plotly_chart(heatmap,use_container_width=True)
        else:
            st.warning("No numerical columns available for heatmap.")

        # ---------------- AUTOMATIC GRAPHS ---------------- #
        st.header("Automatic Graph Generation")
        auto_graphs = (visualizer.generate_automatic_graphs())
        if len(auto_graphs) == 0:
            st.warning("No graphs generated.")
        else:
            for fig in auto_graphs:
                st.plotly_chart(fig,use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a dataset to begin analysis.")
