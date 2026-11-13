import pandas as pd


def build_audit_summary(
    results: pd.DataFrame,
) -> pd.DataFrame:

    return (
        results
        .groupby(
            "outcome",
            as_index=False,
        )
        .agg(
            account_count=(
                "account_id",
                "count",
            )
        )
        .sort_values(
            "outcome"
        )
        .reset_index(
            drop=True
        )
    )
