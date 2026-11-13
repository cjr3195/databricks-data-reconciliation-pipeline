from pathlib import Path

from src.config import (
    OUTPUT_FILE,
)
from src.pipeline import (
    run_pipeline,
)


def test_pipeline_creates_excel():

    result = run_pipeline()

    assert OUTPUT_FILE.exists()

    assert (
        result["output"]["status"]
        == "VALID"
    )


def test_excel_contains_required_sheets():

    result = run_pipeline()

    assert (
        result["output"][
            "sheet_count"
        ]
        == 5
    )


def test_excel_account_rows_reconcile():

    result = run_pipeline()

    assert (
        result["output"][
            "account_rows"
        ]
        == result["accounts"]
    )
