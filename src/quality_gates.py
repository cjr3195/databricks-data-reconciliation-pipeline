from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class QualityCheck:
    check_id: str
    check_name: str
    status: str
    expected: object
    actual: object
    details: str = ""


class QualityGateError(RuntimeError):
    pass


def create_check(
    check_id: str,
    check_name: str,
    passed: bool,
    expected,
    actual,
    details: str = "",
) -> QualityCheck:

    return QualityCheck(
        check_id=check_id,
        check_name=check_name,
        status="PASS" if passed else "FAIL",
        expected=expected,
        actual=actual,
        details=details,
    )


def validate_required_files(
    file_paths: list[Path],
) -> QualityCheck:

    missing_files = [
        str(file_path)
        for file_path in file_paths
        if not file_path.exists()
    ]

    return create_check(
        check_id="QG01",
        check_name="Required files available",
        passed=not missing_files,
        expected=0,
        actual=len(missing_files),
        details=", ".join(missing_files),
    )


def validate_input_rows(
    organizations: pd.DataFrame,
    professionals: pd.DataFrame,
) -> QualityCheck:

    total_rows = (
        len(organizations)
        + len(professionals)
    )

    return create_check(
        check_id="QG02",
        check_name="Input contains account records",
        passed=total_rows > 0,
        expected="> 0",
        actual=total_rows,
    )


def validate_unique_account_ids(
    accounts: pd.DataFrame,
) -> QualityCheck:

    total_rows = len(accounts)

    unique_accounts = (
        accounts["account_id"]
        .nunique()
    )

    return create_check(
        check_id="QG03",
        check_name="Account IDs are unique",
        passed=total_rows == unique_accounts,
        expected=total_rows,
        actual=unique_accounts,
    )


def validate_universe_coverage(
    accounts: pd.DataFrame,
) -> QualityCheck:

    total_accounts = len(accounts)

    matched_accounts = int(
        accounts["universe_found"]
        .fillna(False)
        .sum()
    )

    return create_check(
        check_id="QG04",
        check_name="Universe reconciliation coverage",
        passed=matched_accounts == total_accounts,
        expected=total_accounts,
        actual=matched_accounts,
    )


def validate_identifier_reconciliation(
    identifiers: pd.DataFrame,
    reconciled: pd.DataFrame,
) -> QualityCheck:

    return create_check(
        check_id="QG05",
        check_name="Identifier rows preserved",
        passed=len(identifiers) == len(reconciled),
        expected=len(identifiers),
        actual=len(reconciled),
    )


def validate_final_rows(
    accounts: pd.DataFrame,
    results: pd.DataFrame,
) -> QualityCheck:

    return create_check(
        check_id="QG06",
        check_name="Final account rows preserved",
        passed=len(accounts) == len(results),
        expected=len(accounts),
        actual=len(results),
    )


def validate_outcomes(
    results: pd.DataFrame,
) -> QualityCheck:

    valid_outcomes = {
        "RESOLVED",
        "PARTIAL_MATCH",
        "MANUAL_REVIEW",
        "ACCOUNT_ENDED",
        "NO_ACTION",
    }

    actual_outcomes = set(
        results["outcome"]
        .dropna()
        .unique()
    )

    invalid_outcomes = (
        actual_outcomes
        - valid_outcomes
    )

    return create_check(
        check_id="QG07",
        check_name="Business outcomes are valid",
        passed=not invalid_outcomes,
        expected=sorted(valid_outcomes),
        actual=sorted(actual_outcomes),
        details=", ".join(
            sorted(invalid_outcomes)
        ),
    )


def validate_address_scores(
    results: pd.DataFrame,
) -> QualityCheck:

    scores = results[
        "address_match_score"
    ].fillna(0)

    valid_scores = (
        scores.between(
            0.0,
            1.0,
            inclusive="both",
        )
        .all()
    )

    return create_check(
        check_id="QG08",
        check_name="Address scores are within range",
        passed=bool(valid_scores),
        expected="0.0 to 1.0",
        actual=(
            f"{scores.min():.4f} "
            f"to {scores.max():.4f}"
        ),
    )


def validate_scenario_expectations(
    results: pd.DataFrame,
    expectations: pd.DataFrame,
) -> QualityCheck:

    actual = results[
        [
            "account_id",
            "scenario_id",
            "outcome",
        ]
    ].rename(
        columns={
            "outcome":
                "actual_outcome",
        }
    )

    comparison = expectations.merge(
        actual,
        how="left",
        on=[
            "account_id",
            "scenario_id",
        ],
        validate="one_to_one",
    )

    comparison["matches_expected"] = (
        comparison["expected_outcome"]
        == comparison["actual_outcome"]
    )

    failed = comparison[
        ~comparison["matches_expected"]
    ]

    details = "; ".join(
        (
            f"{row.account_id}: "
            f"expected={row.expected_outcome}, "
            f"actual={row.actual_outcome}"
        )
        for row in failed.itertuples()
    )

    return create_check(
        check_id="QG09",
        check_name="Account scenarios match expectations",
        passed=failed.empty,
        expected=len(expectations),
        actual=int(
            comparison[
                "matches_expected"
            ].sum()
        ),
        details=details,
    )


def validate_audit_totals(
    results: pd.DataFrame,
    audit_summary: pd.DataFrame,
) -> QualityCheck:

    result_rows = len(results)

    audit_rows = int(
        audit_summary[
            "account_count"
        ].sum()
    )

    return create_check(
        check_id="QG10",
        check_name="Audit totals reconcile",
        passed=result_rows == audit_rows,
        expected=result_rows,
        actual=audit_rows,
    )


def run_quality_gates(
    *,
    required_files: list[Path],
    organizations: pd.DataFrame,
    professionals: pd.DataFrame,
    accounts: pd.DataFrame,
    identifiers: pd.DataFrame,
    reconciled: pd.DataFrame,
    results: pd.DataFrame,
    audit_summary: pd.DataFrame,
    expectations: pd.DataFrame,
) -> dict:

    checks = [
        validate_required_files(
            required_files
        ),
        validate_input_rows(
            organizations,
            professionals,
        ),
        validate_unique_account_ids(
            accounts
        ),
        validate_universe_coverage(
            accounts
        ),
        validate_identifier_reconciliation(
            identifiers,
            reconciled,
        ),
        validate_final_rows(
            accounts,
            results,
        ),
        validate_outcomes(
            results
        ),
        validate_address_scores(
            results
        ),
        validate_scenario_expectations(
            results,
            expectations,
        ),
        validate_audit_totals(
            results,
            audit_summary,
        ),
    ]

    failed_checks = [
        check
        for check in checks
        if check.status == "FAIL"
    ]

    checks_df = pd.DataFrame(
        [
            check.__dict__
            for check in checks
        ]
    )

    if failed_checks:

        failure_details = "; ".join(
            (
                f"{check.check_id} "
                f"{check.check_name}: "
                f"{check.details or check.actual}"
            )
            for check in failed_checks
        )

        raise QualityGateError(
            "Quality gates failed: "
            + failure_details
        )

    return {
        "status": "PASS",
        "quality_checks": len(checks),
        "failed_checks": 0,
        "checks": checks_df,
    }
