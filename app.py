import streamlit as st

from analysis.loader import DatasetLoader
from analysis.schema_detector import SchemaDetector
from analysis.cleaner import DataCleaner

from analysis.analyzer import DataAnalyzer
from analysis.relationship_engine import RelationshipEngine

from analysis.recommendation_engine import (
    RecommendationEngine
)

from analysis.visualizer import Visualizer

from analysis.insight_generator import (
    InsightGenerator
)

# ---------------------------------

st.set_page_config(

    page_title="Smart Dataset Analyzer",

    layout="wide"
)

st.title(
    "📊 Smart Dataset Analysis Platform"
)

# ---------------------------------

uploaded_file = st.file_uploader(

    "Upload CSV or Excel File",

    type=["csv", "xlsx", "xls"]
)

# ---------------------------------

if uploaded_file:

    try:

        # Load

        df = DatasetLoader.load_file(
            uploaded_file
        )

        st.success(
            "Dataset Loaded Successfully"
        )

        st.subheader("Dataset Preview")

        st.dataframe(df.head())

        # Schema Detection

        schema = SchemaDetector(
            df
        ).detect_schema()

        # Cleaning

        df = DataCleaner(
            df,
            schema
        ).clean()

        # Analysis

        analyzer = DataAnalyzer(
            df,
            schema
        )

        analysis_results = (
            analyzer.run_analysis()
        )

        # Relationships

        relationship_engine = (
            RelationshipEngine(
                df,
                schema
            )
        )

        correlation_matrix = (
            relationship_engine
            .correlation_matrix()
        )

        relationships = (
            relationship_engine
            .strong_relationships()
        )

        # Insights

        insights = InsightGenerator(

            df,

            schema,

            analysis_results,

            relationships

        ).generate()

        # ---------------------------------

        st.header("Detected Schema")

        st.json(schema)

        # ---------------------------------

        st.header("Dataset Analysis")

        st.json(analysis_results)

        # ---------------------------------

        st.header("Insights")

        for insight in insights:

            st.success(insight)

        # ---------------------------------

        visualizer = Visualizer(df)

        recommendation_engine = (
            RecommendationEngine(
                df,
                schema
            )
        )

        recommendations = (
            recommendation_engine
            .recommend()
        )

        st.header(
            "Recommended Visualizations"
        )

        graph_count = 0

        MAX_GRAPHS = 10

        for rec in recommendations:

            if graph_count >= MAX_GRAPHS:
                break

            try:

                if rec["type"] == "histogram":

                    fig = visualizer.histogram(
                        rec["column"]
                    )

                elif rec["type"] == "scatter":

                    fig = visualizer.scatter(
                        rec["x"],
                        rec["y"]
                    )

                elif rec["type"] == "bar":

                    fig = visualizer.bar(
                        rec["category"],
                        rec["value"]
                    )

                elif rec["type"] == "line":

                    fig = visualizer.line(
                        rec["date"],
                        rec["value"]
                    )

                else:

                    continue

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                graph_count += 1

            except Exception as e:

                continue

        # ---------------------------------

        st.header("Correlation Heatmap")

        heatmap = visualizer.heatmap(
            correlation_matrix
        )

        if heatmap is not None:

            st.plotly_chart(
                heatmap,
                use_container_width=True
            )

        else:

            st.info(
                "Not enough numeric columns "
                "to generate heatmap."
            )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )
