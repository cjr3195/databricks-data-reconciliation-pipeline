import pandas as pd


def _split_identifiers(value):
    if pd.isna(value):
        return []

    return [
        item.strip()
        for item in str(value).split(";")
        if item.strip()
    ]


def extract_identifiers(
    enriched_accounts: pd.DataFrame,
) -> pd.DataFrame:

    records = []

    for _, row in (
        enriched_accounts.iterrows()
    ):

        for identifier in _split_identifiers(
            row.get(
                "primary_identifier"
            )
        ):
            records.append({
                "account_id":
                    row["account_id"],
                "scenario_id":
                    row["scenario_id"],
                "entity_type":
                    row["entity_type"],
                "identifier":
                    identifier,
                "identifier_type":
                    "PRIMARY",
            })

        for identifier in _split_identifiers(
            row.get(
                "secondary_identifier"
            )
        ):
            records.append({
                "account_id":
                    row["account_id"],
                "scenario_id":
                    row["scenario_id"],
                "entity_type":
                    row["entity_type"],
                "identifier":
                    identifier,
                "identifier_type":
                    "SECONDARY",
            })

    return (
        pd.DataFrame(records)
        .drop_duplicates()
        .reset_index(drop=True)
    )
