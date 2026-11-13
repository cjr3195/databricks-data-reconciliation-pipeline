import pandas as pd

from src.address_matching import (
    address_match_score,
    addresses_match,
)
from src.audit import (
    build_audit_summary,
)
from src.business_rules import (
    determine_outcome,
)
from src.config import (
    ACCOUNT_EXPECTATIONS_FILE,
    EXPECTATIONS_FILE,
    INPUT_FILE,
    ORGANIZATIONS_SHEET,
    PROFESSIONALS_SHEET,
    REGISTRY_FILE,
    UNIVERSE_FILE,
)
from src.enrichment import (
    build_identifier_summary,
    enrich_accounts_with_registry,
)
from src.identifiers import (
    extract_identifiers,
)
from src.ingestion import (
    load_weekly_report,
)
from src.quality_gates import (
    run_quality_gates,
)
from src.reference_lookup import (
    load_identifier_registry,
    reconcile_identifiers,
)
from src.universe import (
    combine_accounts,
    enrich_with_universe,
    load_universe,
)


def _prepare_numeric_columns(
    results: pd.DataFrame,
) -> pd.DataFrame:
    """
    Ensure reconciliation metrics are numeric and
    have deterministic zero values when missing.
    """

    results = results.copy()

    numeric_columns = [
        "identifiers_total",
        "identifiers_found",
        "active_identifiers",
    ]

    for column in numeric_columns:

        results[column] = (
            results[column]
            .fillna(0)
            .astype(int)
        )

    return results


def _apply_address_matching(
    results: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compare each input address against the
    cleaned reference address.
    """

    results = results.copy()

    results["address_match_score"] = (
        results.apply(
            lambda row: address_match_score(
                row.get("address"),
                row.get(
                    "reference_address"
                ),
            ),
            axis=1,
        )
    )

    results["address_match"] = (
        results.apply(
            lambda row: addresses_match(
                row.get("address"),
                row.get(
                    "reference_address"
                ),
            ),
            axis=1,
        )
    )

    return results


def _apply_business_rules(
    results: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply deterministic business outcomes to
    each reconciled account.
    """

    results = results.copy()

    results["outcome"] = (
        results.apply(
            determine_outcome,
            axis=1,
        )
    )

    return results


def run_pipeline() -> dict:
    """
    Execute the complete portfolio-safe
    reconciliation pipeline.
    """

    # =====================================================
    # 01 - INGESTION
    # =====================================================

    weekly = load_weekly_report(
        INPUT_FILE,
        ORGANIZATIONS_SHEET,
        PROFESSIONALS_SHEET,
    )

    organizations = (
        weekly["organizations"]
    )

    professionals = (
        weekly["professionals"]
    )

    # =====================================================
    # 02 - ACCOUNT CONSOLIDATION
    # =====================================================

    accounts = combine_accounts(
        organizations,
        professionals,
    )

    # =====================================================
    # 03 - ACCOUNT UNIVERSE
    # =====================================================

    universe = load_universe(
        UNIVERSE_FILE
    )

    accounts = enrich_with_universe(
        accounts,
        universe,
    )

    # =====================================================
    # 04 - IDENTIFIER EXTRACTION
    # =====================================================

    identifiers = extract_identifiers(
        accounts
    )

    # =====================================================
    # 05 - REFERENCE REGISTRY
    # =====================================================

    registry = load_identifier_registry(
        REGISTRY_FILE
    )

    reconciled = reconcile_identifiers(
        identifiers,
        registry,
    )

    # =====================================================
    # 06 - CLEANING + IDENTIFIER SUMMARY
    # =====================================================

    identifier_summary = (
        build_identifier_summary(
            reconciled
        )
    )

    # =====================================================
    # 07 - ENRICHMENT
    # =====================================================

    results = (
        enrich_accounts_with_registry(
            accounts,
            identifier_summary,
        )
    )

    results = _prepare_numeric_columns(
        results
    )

    # =====================================================
    # 08 - ADDRESS MATCHING
    # =====================================================

    results = _apply_address_matching(
        results
    )

    # =====================================================
    # 09 - BUSINESS RULES
    # =====================================================

    results = _apply_business_rules(
        results
    )

    # =====================================================
    # 10 - AUDIT
    # =====================================================

    audit_summary = (
        build_audit_summary(
            results
        )
    )

    # =====================================================
    # 11 - EXPECTED RESULTS
    # =====================================================

    expectations = pd.read_csv(
        ACCOUNT_EXPECTATIONS_FILE,
        dtype=str,
    )

    # =====================================================
    # 12 - QUALITY GATES
    # =====================================================

    quality = run_quality_gates(
        required_files=[
            INPUT_FILE,
            UNIVERSE_FILE,
            REGISTRY_FILE,
            EXPECTATIONS_FILE,
            ACCOUNT_EXPECTATIONS_FILE,
        ],
        organizations=organizations,
        professionals=professionals,
        accounts=accounts,
        identifiers=identifiers,
        reconciled=reconciled,
        results=results,
        audit_summary=audit_summary,
        expectations=expectations,
    )

    # =====================================================
    # SUMMARY METRICS
    # =====================================================

    universe_matches = int(
        accounts["universe_found"]
        .fillna(False)
        .sum()
    )

    identifier_matches = int(
        reconciled["registry_found"]
        .fillna(False)
        .sum()
    )

    address_matches = int(
        results["address_match"]
        .fillna(False)
        .sum()
    )

    manual_review = int(
        (
            results["outcome"]
            == "MANUAL_REVIEW"
        ).sum()
    )

    # =====================================================
    # PIPELINE RESULT
    # =====================================================

    return {
        "status":
            "SUCCESS",

        "organizations":
            len(organizations),

        "professionals":
            len(professionals),

        "accounts":
            len(accounts),

        "universe_matches":
            universe_matches,

        "identifiers":
            len(identifiers),

        "identifier_matches":
            identifier_matches,

        "address_matches":
            address_matches,

        "manual_review":
            manual_review,

        "quality_status":
            quality["status"],

        "quality_checks":
            quality[
                "quality_checks"
            ],

        "failed_checks":
            quality[
                "failed_checks"
            ],

        # Detailed pipeline artifacts
        "results":
            results,

        "identifier_audit":
            reconciled,

        "audit_summary":
            audit_summary,

        "quality_details":
            quality["checks"],
    }


def _build_console_summary(
    result: dict,
) -> dict:
    """
    Return only lightweight metrics for console
    output. DataFrames remain available in the
    full pipeline result.
    """

    excluded_keys = {
        "results",
        "identifier_audit",
        "audit_summary",
        "quality_details",
    }

    return {
        key: value
        for key, value in result.items()
        if key not in excluded_keys
    }


if __name__ == "__main__":

    pipeline_result = (
        run_pipeline()
    )

    print(
        _build_console_summary(
            pipeline_result
        )
    )
