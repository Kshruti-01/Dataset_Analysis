import streamlit as st

from analysis.loader import DatasetLoader
from analysis.schema_detector import SchemaDetector
from analysis.cleaner import DataCleaner
from analysis.profiler import DatasetProfiler
from analysis.relationship_engine import RelationshipEngine
from analysis.recommendation_engine import RecommendationEngine
from analysis.visualizer import Visualizer
from analysis.insight_generator import InsightGenerator


st.set_page_config(

    page_title="Smart Dataset Analyzer",

    layout="wide"
)

st.title(

    "📊 Smart Dataset Analysis Platform"
)

uploaded_file = st.file_uploader(

    "Upload CSV / Excel",

    type=["csv", "xlsx", "xls"]
)

if uploaded_file:

    # Load

    df = DatasetLoader.load_file(

        uploaded_file
    )

    # Detect Schema

    schema = SchemaDetector(

        df
    ).detect_schema()

    # Clean

    df = DataCleaner(

        df,

        schema
    ).clean()

    # Profile

    profiler = DatasetProfiler(df)

    st.header(

        "Dataset Profile"
    )

    st.json(

        profiler.generate_profile()
    )

    st.metric(

        "Quality Score",

        profiler.quality_score()
    )

    st.header(

        "Detected Schema"
    )

    st.json(schema)

    # Relationships

    relationship_engine = (

        RelationshipEngine(

            df,

            schema
        )
    )

    corr_matrix = (

        relationship_engine
        .correlation_analysis()
    )

    relationships = (

        relationship_engine
        .strong_relationships()
    )

    # Insights

    insight_generator = (

        InsightGenerator(

            df,

            schema,

            relationships
        )
    )

    st.header(

        "Insights"
    )

    for insight in (

        insight_generator
        .generate()
    ):

        st.success(insight)

    # Visuals

    visualizer = Visualizer(df)

    recommendation_engine = (

        RecommendationEngine(

            df,

            schema
        )
    )

    recommendations = (

        recommendation_engine
        .recommend_visualizations()
    )

    st.header(

        "Visualizations"
    )

    graph_count = 0

    for rec in recommendations:

        if graph_count >= 15:

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

        except Exception:

            continue

    st.header(
        "Correlation Heatmap"
    )

    heatmap = visualizer.heatmap(
        corr_matrix
    )

    if heatmap:

        st.plotly_chart(
            heatmap,
            use_container_width=True
        )
