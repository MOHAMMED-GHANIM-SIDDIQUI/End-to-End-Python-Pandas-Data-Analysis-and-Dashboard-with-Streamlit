import pandas as pd

from churn_dashboard.analytics import customer_statistics, future_insights
from churn_dashboard.schema import validate_dataset


def sample_churn_df():
    return pd.DataFrame(
        {
            "CustomerID": [1, 2],
            "Age": [30, 40],
            "Gender": ["Male", "Female"],
            "Tenure": [10, 20],
            "Usage Frequency": [5, 7],
            "Support Calls": [1, 3],
            "Payment Delay": [2, 4],
            "Subscription Type": ["Basic", "Premium"],
            "Contract Length": ["Monthly", "Annual"],
            "Total Spend": [100.0, 300.0],
            "Last Interaction": [5, 10],
            "Churn": [0, 1],
        }
    )


def test_validate_dataset_accepts_required_schema():
    assert validate_dataset(sample_churn_df()) == []


def test_validate_dataset_reports_missing_columns():
    errors = validate_dataset(pd.DataFrame({"Age": [1]}))

    assert errors
    assert "Missing required columns" in errors[0]


def test_customer_statistics_uses_named_columns():
    stats = customer_statistics(sample_churn_df())

    assert stats["Average Age"] == 35
    assert stats["Churn Rate (%)"] == 50


def test_future_insights_returns_projection_keys():
    insights = future_insights(sample_churn_df())

    assert "Projected Total Spend Next Year" in insights
    assert insights["Projected Subscription Upgrades"] == 0.15
