import pandas as pd


REQUIRED_COLUMNS = {
    "CustomerID",
    "Age",
    "Gender",
    "Tenure",
    "Usage Frequency",
    "Support Calls",
    "Payment Delay",
    "Subscription Type",
    "Contract Length",
    "Total Spend",
    "Last Interaction",
    "Churn",
}


def validate_dataset(df: pd.DataFrame) -> list[str]:
    errors = []
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
    if df.empty:
        errors.append("Dataset is empty.")
    return errors
