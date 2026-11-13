from src.config import (
    INPUT_FILE,
    ORGANIZATIONS_SHEET,
    PROFESSIONALS_SHEET,
)
from src.ingestion import (
    load_weekly_report,
)


def test_loads_required_sheets():

    weekly = load_weekly_report(
        INPUT_FILE,
        ORGANIZATIONS_SHEET,
        PROFESSIONALS_SHEET,
    )

    assert len(
        weekly["organizations"]
    ) == 10

    assert len(
        weekly["professionals"]
    ) == 8


def test_input_contains_account_ids():

    weekly = load_weekly_report(
        INPUT_FILE,
        ORGANIZATIONS_SHEET,
        PROFESSIONALS_SHEET,
    )

    assert (
        weekly["organizations"][
            "account_id"
        ]
        .notna()
        .all()
    )

    assert (
        weekly["professionals"][
            "account_id"
        ]
        .notna()
        .all()
    )
