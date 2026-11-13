from src.address_matching import (
    address_match_score,
    addresses_match,
    normalize_address,
)


def test_normalizes_street_abbreviation():

    assert normalize_address(
        "245 Northwind Street"
    ) == normalize_address(
        "245 Northwind St"
    )


def test_normalizes_road_abbreviation():

    assert normalize_address(
        "800 Cloud Road"
    ) == normalize_address(
        "800 Cloud Rd"
    )


def test_exact_address_matches():

    assert addresses_match(
        "100 Innovation Way",
        "100 Innovation Way",
    )


def test_abbreviated_address_matches():

    assert addresses_match(
        "55 Analytics Avenue",
        "55 Analytics Ave",
    )


def test_different_address_does_not_match():

    assert not addresses_match(
        "100 Innovation Way",
        "999 Review Drive",
    )


def test_score_is_bounded():

    score = address_match_score(
        "100 Innovation Way",
        "100 Innovation Way",
    )

    assert 0.0 <= score <= 1.0
    assert score == 1.0
