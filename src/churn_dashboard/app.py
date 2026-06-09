from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from .analytics import about_df, customer_statistics, future_insights
from .schema import validate_dataset


APP_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = APP_DIR / "data" / "churn_dataset.csv"


@st.cache_data(show_spinner=False)
def load_default_dataset() -> pd.DataFrame:
    return pd.read_csv(DEFAULT_DATASET)


def render_matplotlib_chart(title: str, plot_fn) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    try:
        plot_fn(ax)
        ax.set_title(title)
        fig.tight_layout()
        st.pyplot(fig)
    finally:
        plt.close(fig)


def render_dashboard(df: pd.DataFrame) -> None:
    st.subheader("Customer Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customers", f"{len(df):,}")
    c2.metric("Churn Rate", f"{df['Churn'].mean() * 100:.2f}%")
    c3.metric("Total Spend", f"{df['Total Spend'].sum():,.0f}")
    c4.metric("Avg Support Calls", f"{df['Support Calls'].mean():.2f}")

    col1, col2 = st.columns(2)
    with col1:
        render_matplotlib_chart(
            "Distribution of Age",
            lambda ax: df["Age"].plot(kind="hist", bins=10, color="skyblue", edgecolor="black", ax=ax),
        )
    with col2:
        render_matplotlib_chart(
            "Average Total Spend by Subscription Type",
            lambda ax: df.groupby("Subscription Type")["Total Spend"].mean().plot(kind="bar", color="lightgreen", ax=ax),
        )

    col1, col2 = st.columns(2)
    with col1:
        render_matplotlib_chart(
            "Gender Distribution",
            lambda ax: df["Gender"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax, ylabel=""),
        )
    with col2:
        render_matplotlib_chart(
            "Total Spend by Contract Length",
            lambda ax: df.groupby("Contract Length")["Total Spend"].sum().plot(kind="pie", autopct="%1.1f%%", ax=ax, ylabel=""),
        )

    col1, col2 = st.columns(2)
    with col1:
        render_matplotlib_chart(
            "Churn Rate by Gender",
            lambda ax: (df.groupby("Gender")["Churn"].mean() * 100).plot(kind="bar", color="coral", ax=ax),
        )
    with col2:
        def age_by_gender(ax):
            for gender, color in [("Male", "blue"), ("Female", "red")]:
                subset = df[df["Gender"] == gender]
                if not subset.empty:
                    subset["Age"].plot(kind="hist", bins=10, alpha=0.5, color=color, label=gender, ax=ax)
            ax.legend()

        render_matplotlib_chart("Age Distribution by Gender", age_by_gender)


def render_dataset_profile(df: pd.DataFrame) -> None:
    df_sample, size, info, columns, missing_values, stats = about_df(df)
    st.subheader("Dataset Profile")
    st.metric("Rows", f"{size:,}")
    st.write("Sample")
    st.dataframe(df_sample, use_container_width=True)
    st.write("Column types")
    st.dataframe(columns.rename("dtype"), use_container_width=True)
    st.write("Missing values")
    st.dataframe(missing_values.rename("missing"), use_container_width=True)
    st.write("Statistics")
    st.dataframe(stats, use_container_width=True)
    with st.expander("Raw dataframe info"):
        st.text(info)


def main() -> None:
    st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")
    st.title("Customer Churn Dashboard")
    st.caption("Pandas and Streamlit dashboard for customer churn exploration and executive-style insights.")

    st.sidebar.title("Data Source")
    source = st.sidebar.radio("Choose dataset", ["Built-in churn dataset", "Upload CSV"])

    try:
        if source == "Upload CSV":
            uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file is None:
                st.info("Upload a CSV file or switch to the built-in churn dataset.")
                return
            df = pd.read_csv(uploaded_file)
        else:
            df = load_default_dataset()

        errors = validate_dataset(df)
        if errors:
            for error in errors:
                st.error(error)
            st.stop()

        section = st.sidebar.radio("View", ["Dashboard", "Customer Statistics", "Future Insights", "About Dataset"])

        if section == "Dashboard":
            render_dashboard(df)
        elif section == "Customer Statistics":
            st.subheader("Customer Statistics")
            for key, value in customer_statistics(df).items():
                st.metric(key, f"{value:,.2f}")
        elif section == "Future Insights":
            st.subheader("Future Insights")
            st.caption("Simple projections based on current averages. These are directional analytics, not forecasts.")
            for key, value in future_insights(df).items():
                st.metric(key, f"{value:,.2f}")
        else:
            render_dataset_profile(df)
    except Exception as exc:
        st.error(f"Dashboard error: {exc}")

    st.markdown("---")
    st.caption("Created by Mohammed Ghanim Siddiqui")
