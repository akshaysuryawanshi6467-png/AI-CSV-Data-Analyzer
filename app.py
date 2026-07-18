import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="AI CSV Data Analyzer",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("📊 Dashboard")

show_data = st.sidebar.checkbox("Show Dataset", True)
show_summary = st.sidebar.checkbox("Show Summary", True)
show_charts = st.sidebar.checkbox("Show Charts", True)
show_insights = st.sidebar.checkbox("Show Business Insights", True)


st.title("📊 AI CSV Data Analyzer")
st.markdown("Analyze your CSV file with interactive charts and insights.")


uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("✅ Dataset Uploaded Successfully!")


    if show_data:

        st.subheader("📄 Dataset Preview")
        st.dataframe(df, use_container_width=True)


    st.subheader("🔍 Search Product")

    if "Product" in df.columns:

        search = st.text_input("Search Product Name")

        if search:

            filtered = df[
                df["Product"].astype(str).str.contains(
                    search,
                    case=False
                )
            ]

            st.dataframe(filtered)

        else:
            filtered = df

    else:

        filtered = df
        st.info("No 'Product' column found. Search disabled.")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicate Rows", int(df.duplicated().sum()))

    if show_summary:

        st.divider()

        st.subheader("📊 Summary Statistics")

        st.dataframe(
            df.describe(),
            use_container_width=True
        )


    st.divider()

    st.subheader("❗ Missing Values")

    st.dataframe(df.isnull().sum())

    numeric_columns = df.select_dtypes(include="number").columns

    if show_charts and len(numeric_columns) > 0:

        st.divider()

        st.subheader("📈 Interactive Charts")

        chart = st.selectbox(
            "Choose Chart",
            [
                "Bar",
                "Line",
                "Scatter",
                "Pie",
                "Histogram"
            ]
        )

        column = st.selectbox(
            "Choose Numeric Column",
            numeric_columns
        )

        if chart == "Bar":

            if "Product" in df.columns:
                fig = px.bar(
                    df,
                    x="Product",
                    y=column,
                    color="Product"
                )
            else:
                fig = px.bar(df, y=column)

        elif chart == "Line":

            if "Product" in df.columns:
                fig = px.line(
                    df,
                    x="Product",
                    y=column,
                    markers=True
                )
            else:
                fig = px.line(df, y=column)

        elif chart == "Scatter":

            if len(numeric_columns) >= 2:

                fig = px.scatter(
                    df,
                    x=numeric_columns[0],
                    y=numeric_columns[1],
                    color="Product" if "Product" in df.columns else None
                )

            else:

                st.warning("Need at least two numeric columns.")
                fig = None

        elif chart == "Pie":

            if "Product" in df.columns:

                fig = px.pie(
                    df,
                    names="Product",
                    values=column
                )

            else:

                st.warning("Pie chart requires a Product column.")
                fig = None

        elif chart == "Histogram":

            fig = px.histogram(
                df,
                x=column
            )

        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)

    if show_insights:

        st.divider()

        st.subheader("📈 Business Insights")

        for col in numeric_columns:

            st.success(f"Highest {col}: {df[col].max()}")

            st.info(f"Average {col}: {df[col].mean():.2f}")

            st.warning(f"Lowest {col}: {df[col].min()}")


    st.divider()

    st.subheader("⬇ Download Filtered Data")

    csv = filtered.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

else:

    st.info("📁 Please upload a CSV file.")