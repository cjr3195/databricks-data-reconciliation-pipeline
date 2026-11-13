import pandas as pd

from src.address_cleaning import (
    clean_reference_address,
)


def build_identifier_summary(
    reconciled: pd.DataFrame,
) -> pd.DataFrame:

    df = reconciled.copy()

    df["clean_reference_address"] = (
        df["registry_raw_address"]
        .apply(clean_reference_address)
    )

    summary = (
        df.groupby(
            "account_id",
            as_index=False,
        )
        .agg(
            identifiers_total=(
                "identifier",
                "count",
            ),
            identifiers_found=(
                "registry_found",
                "sum",
            ),
            active_identifiers=(
                "registry_status",
                lambda values: sum(
                    str(value).upper()
                    == "ACTIVE"
                    for value in values
                ),
            ),
            reference_address=(
                "clean_reference_address",
                "first",
            ),
        )
    )

    return summary


def enrich_accounts_with_registry(
    accounts: pd.DataFrame,
    identifier_summary: pd.DataFrame,
) -> pd.DataFrame:

    return accounts.merge(
        identifier_summary,
        how="left",
        on="account_id",
        validate="one_to_one",
    )
