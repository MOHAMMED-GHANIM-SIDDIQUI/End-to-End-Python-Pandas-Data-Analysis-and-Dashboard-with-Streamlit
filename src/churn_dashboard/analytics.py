import io

import pandas as pd


def about_df(df: pd.DataFrame) -> tuple[pd.DataFrame, int, str, pd.Series, pd.Series, pd.DataFrame]:
    sample_size = min(10, len(df))
    df_sample = df.sample(sample_size, random_state=42) if sample_size else df
    buffer = io.StringIO()
    df.info(buf=buffer)
    info = buffer.getvalue()
    columns = df.dtypes
    missing_values = df.isnull().sum()
    stats = df.describe(include="all")
    return df_sample, len(df), info, columns, missing_values, stats


def customer_statistics(df: pd.DataFrame) -> dict[str, float]:
    return {
        "Average Age": df["Age"].mean(),
        "Average Tenure": df["Tenure"].mean(),
        "Total Spend": df["Total Spend"].sum(),
        "Average Support Calls": df["Support Calls"].mean(),
        "Churn Rate (%)": df["Churn"].mean() * 100,
        "Payment Delay Std Dev": df["Payment Delay"].std(),
    }


def future_insights(df: pd.DataFrame) -> dict[str, float]:
    average_monthly_spend = df["Total Spend"].mean()
    churn_rate = df["Churn"].mean()
    average_support_calls = df["Support Calls"].mean()
    average_payment_delay = df["Payment Delay"].mean()
    standard_and_basic_users = df[df["Subscription Type"].isin(["Standard", "Basic"])]
    average_tenure = df["Tenure"].mean()

    return {
        "Projected Total Spend Next Year": average_monthly_spend * 12 * len(df),
        "Projected Churn Next Year": churn_rate * len(df),
        "Projected Support Calls Increase": average_support_calls * 1.1,
        "Projected Payment Delay Increase": average_payment_delay * 1.05,
        "Projected Subscription Upgrades": len(standard_and_basic_users) * 0.15,
        "Projected Tenure Growth": average_tenure * 1.2,
    }
