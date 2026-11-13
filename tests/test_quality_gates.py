import pandas as pd

from src.quality_gates import (
    validate_address_scores,
    validate_outcomes,
    validate_unique_account_ids,
)


def test_unique_account_gate_passes():

    accounts = pd.DataFrame({
        "account_id": [
            "A-001",
            "A-002",
        ]
    })

    check = validate_unique_account_ids(
        accounts
    )

    assert check.status == "PASS"


def test_unique_account_gate_fails():

    accounts = pd.DataFrame({
        "account_id": [
            "A-001",
            "A-001",
        ]
    })

    check = validate_unique_account_ids(
        accounts
    )

    assert check.status == "FAIL"


def test_invalid_outcome_fails():

    results = pd.DataFrame({
        "outcome": [
            "RESOLVED",
            "UNKNOWN_RESULT",
        ]
    })

    check = validate_outcomes(
        results
    )

    assert check.status == "FAIL"


def test_invalid_score_fails():

    results = pd.DataFrame({
        "address_match_score": [
            0.8,
            1.4,
        ]
    })

    check = validate_address_scores(
        results
    )

    assert check.status == "FAIL"
