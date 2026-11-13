import re


ABBREVIATIONS = {
    "STREET": "ST",
    "ROAD": "RD",
    "AVENUE": "AVE",
    "BOULEVARD": "BLVD",
    "DRIVE": "DR",
    "LANE": "LN",
    "COURT": "CT",
    "PLACE": "PL",
    "SUITE": "STE",
    "APARTMENT": "APT",
}


def normalize_address(value):

    if value is None:
        return ""

    text = re.sub(
        r"[^A-Z0-9 ]",
        " ",
        str(value).upper(),
    )

    tokens = [
        token
        for token in text.split()
        if token
    ]

    normalized = [
        ABBREVIATIONS.get(
            token,
            token,
        )
        for token in tokens
    ]

    return " ".join(normalized)


def address_match_score(
    left,
    right,
) -> float:

    left_tokens = set(
        normalize_address(left).split()
    )

    right_tokens = set(
        normalize_address(right).split()
    )

    if not left_tokens or not right_tokens:
        return 0.0

    intersection = (
        left_tokens & right_tokens
    )

    union = (
        left_tokens | right_tokens
    )

    return round(
        len(intersection)
        / len(union),
        4,
    )


def addresses_match(
    left,
    right,
    threshold=0.75,
) -> bool:

    return (
        address_match_score(
            left,
            right,
        )
        >= threshold
    )
