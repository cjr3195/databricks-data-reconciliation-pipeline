def determine_outcome(row) -> str:

    if (
        str(
            row.get(
                "account_end_status",
                ""
            )
        ).upper()
        == "ENDED"
    ):
        return "ACCOUNT_ENDED"

    if (
        str(
            row.get(
                "account_category",
                ""
            )
        ).upper()
        == "SPECIAL"
    ):
        return "NO_ACTION"

    total = int(
        row.get(
            "identifiers_total",
            0,
        )
        or 0
    )

    found = int(
        row.get(
            "identifiers_found",
            0,
        )
        or 0
    )

    active = int(
        row.get(
            "active_identifiers",
            0,
        )
        or 0
    )

    if total == 0:
        return "MANUAL_REVIEW"

    if found == 0:
        return "MANUAL_REVIEW"

    if found < total:
        return "PARTIAL_MATCH"

    if active == 0:
        return "MANUAL_REVIEW"

    return "RESOLVED"
