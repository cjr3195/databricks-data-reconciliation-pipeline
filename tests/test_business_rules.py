import pandas as pd

from src.business_rules import (
    determine_outcome,
)


def make_row(**overrides):

    values = {
        "account_end_status": "ACTIVE",
        "account_category": "STANDARD",
        "identifiers_total": 2,
        "identifiers_found": 2,
        "active_identifiers": 2,
    }

    values.update(
        overrides
    )

    return pd.Series(values)


def test_ended_account_has_priority():

    outcome = determine_outcome(
        make_row(
            account_end_status="ENDED",
            account_category="SPECIAL",
        )
    )

    assert outcome == "ACCOUNT_ENDED"


def test_special_account_returns_no_action():

    outcome = determine_outcome(
        make_row(
            account_category="SPECIAL",
        )
    )

    assert outcome == "NO_ACTION"


def test_no_identifiers_requires_review():

    outcome = determine_outcome(
        make_row(
            identifiers_total=0,
            identifiers_found=0,
            active_identifiers=0,
        )
    )

    assert outcome == "MANUAL_REVIEW"


def test_partial_identifier_match():

    outcome = determine_outcome(
        make_row(
            identifiers_total=2,
            identifiers_found=1,
        )
    )

    assert outcome == "PARTIAL_MATCH"


def test_inactive_identifiers_require_review():

    outcome = determine_outcome(
        make_row(
            identifiers_total=2,
            identifiers_found=2,
            active_identifiers=0,
        )
    )

    assert outcome == "MANUAL_REVIEW"


def test_full_reconciliation():

    outcome = determine_outcome(
        make_row()
    )

    assert outcome == "RESOLVED"
