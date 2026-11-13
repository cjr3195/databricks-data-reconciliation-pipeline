import pandas as pd


REQUIRED_UNIVERSE_COLUMNS = {
    "account_id",
    "account_name",
    "primary_identifier",
    "secondary_identifier",
    "identifier_status",
    "canonical_address",
    "account_category",
    "account_end_status",
    "last_activity_date",
    "distribution_method",
    "parent_contract",
}


def load_universe(
    file_path,
) -> pd.DataFrame:

    df = pd.read_csv(
        file_path,
        dtype=str,
    )

    missing = (
        REQUIRED_UNIVERSE_COLUMNS
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            "Account Universe is missing columns: "
            + ", ".join(sorted(missing))
        )

    return df


def combine_accounts(
    organizations: pd.DataFrame,
    professionals: pd.DataFrame,
) -> pd.DataFrame:

    organizations = (
        organizations
        .copy()
        .assign(entity_type="ORGANIZATION")
    )

    professionals = (
        professionals
        .copy()
        .assign(entity_type="PROFESSIONAL")
    )

    return pd.concat(
        [
            organizations,
            professionals,
        ],
        ignore_index=True,
    )


def enrich_with_universe(
    accounts: pd.DataFrame,
    universe: pd.DataFrame,
) -> pd.DataFrame:

    enriched = accounts.merge(
        universe,
        how="left",
        on="account_id",
        suffixes=(
            "_input",
            "_universe",
        ),
        validate="many_to_one",
    )

    enriched["universe_found"] = (
        enriched[
            "primary_identifier"
        ].notna()
    )

    return enriched
