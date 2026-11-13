from src.audit import build_audit_summary
from src.business_rules import (
    determine_outcome,
)
from src.config import (
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
from src.reference_lookup import (
    load_identifier_registry,
    reconcile_identifiers,
)
from src.universe import (
    combine_accounts,
    enrich_with_universe,
    load_universe,
)


def run_pipeline():

    weekly = load_weekly_report(
        INPUT_FILE,
        ORGANIZATIONS_SHEET,
        PROFESSIONALS_SHEET,
    )

    accounts = combine_accounts(
        weekly["organizations"],
        weekly["professionals"],
    )

    universe = load_universe(
        UNIVERSE_FILE
    )

    accounts = enrich_with_universe(
        accounts,
        universe,
    )

    identifiers = extract_identifiers(
        accounts
    )

    registry = load_identifier_registry(
        REGISTRY_FILE
    )

    reconciled = reconcile_identifiers(
        identifiers,
        registry,
    )

    identifier_summary = (
        build_identifier_summary(
            reconciled
        )
    )

    results = (
        enrich_accounts_with_registry(
            accounts,
            identifier_summary,
        )
    )

    results[
        "identifiers_total"
    ] = (
        results[
            "identifiers_total"
        ]
        .fillna(0)
        .astype(int)
    )

    results[
        "identifiers_found"
    ] = (
        results[
            "identifiers_found"
        ]
        .fillna(0)
        .astype(int)
    )

    results[
        "active_identifiers"
    ] = (
        results[
            "active_identifiers"
        ]
        .fillna(0)
        .astype(int)
    )

    results["outcome"] = (
        results.apply(
            determine_outcome,
            axis=1,
        )
    )

    audit_summary = (
        build_audit_summary(
            results
        )
    )

    return {
        "status":
            "SUCCESS",

        "organizations":
            len(
                weekly[
                    "organizations"
                ]
            ),

        "professionals":
            len(
                weekly[
                    "professionals"
                ]
            ),

        "accounts":
            len(accounts),

        "universe_matches":
            int(
                accounts[
                    "universe_found"
                ].sum()
            ),

        "identifiers":
            len(identifiers),

        "identifier_matches":
            int(
                reconciled[
                    "registry_found"
                ].sum()
            ),

        "manual_review":
            int(
                (
                    results["outcome"]
                    == "MANUAL_REVIEW"
                ).sum()
            ),

        "results":
            results,

        "identifier_audit":
            reconciled,

        "audit_summary":
            audit_summary,
    }


if __name__ == "__main__":

    result = run_pipeline()

    summary = {
        key: value
        for key, value in result.items()
        if key not in {
            "results",
            "identifier_audit",
            "audit_summary",
        }
    }

    print(summary)
