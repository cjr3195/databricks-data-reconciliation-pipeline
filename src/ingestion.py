from pathlib import Path

import pandas as pd


REQUIRED_ACCOUNT_COLUMNS = {
    "scenario_id",
    "account_id",
    "account_name",
    "current_identifier",
    "address",
    "city",
    "state",
    "postal_code",
    "account_type",
    "status",
}


def validate_input_file(
    file_path: Path,
) -> None:

    if not file_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    if file_path.stat().st_size == 0:
        raise ValueError(
            "Input workbook is empty."
        )


def _validate_columns(
    df: pd.DataFrame,
    dataset_name: str,
) -> None:

    missing = (
        REQUIRED_ACCOUNT_COLUMNS
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            f"{dataset_name} is missing columns: "
            + ", ".join(sorted(missing))
        )


def load_account_sheet(
    file_path: Path,
    sheet_name: str,
) -> pd.DataFrame:

    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        dtype=str,
        engine="openpyxl",
    )

    df = (
        df
        .dropna(how="all")
        .reset_index(drop=True)
    )

    _validate_columns(
        df,
        sheet_name,
    )

    return df


def load_weekly_report(
    file_path: Path,
    organizations_sheet: str,
    professionals_sheet: str,
) -> dict[str, pd.DataFrame]:

    validate_input_file(
        file_path
    )

    organizations = load_account_sheet(
        file_path,
        organizations_sheet,
    )

    professionals = load_account_sheet(
        file_path,
        professionals_sheet,
    )

    return {
        "organizations": organizations,
        "professionals": professionals,
    }
