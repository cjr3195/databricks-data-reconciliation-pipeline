import pandas as pd


REQUIRED_REGISTRY_COLUMNS = {
    "identifier",
    "identifier_type",
    "status",
    "entity_name",
    "raw_address",
    "city",
    "state",
    "postal_code",
}


def load_identifier_registry(
    file_path,
) -> pd.DataFrame:

    df = pd.read_csv(
        file_path,
        dtype=str,
    )

    missing = (
        REQUIRED_REGISTRY_COLUMNS
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            "Identifier Registry is missing columns: "
            + ", ".join(sorted(missing))
        )

    return df


def reconcile_identifiers(
    identifiers: pd.DataFrame,
    registry: pd.DataFrame,
) -> pd.DataFrame:

    registry_lookup = (
        registry
        .rename(
            columns={
                "status":
                    "registry_status",
                "entity_name":
                    "registry_entity_name",
                "raw_address":
                    "registry_raw_address",
                "city":
                    "registry_city",
                "state":
                    "registry_state",
                "postal_code":
                    "registry_postal_code",
            }
        )
    )

    reconciled = identifiers.merge(
        registry_lookup,
        how="left",
        on=[
            "identifier",
            "identifier_type",
        ],
        validate="many_to_one",
    )

    reconciled[
        "registry_found"
    ] = (
        reconciled[
            "registry_entity_name"
        ].notna()
    )

    return reconciled
