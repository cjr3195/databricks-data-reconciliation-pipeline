from src.address_cleaning import (
    clean_reference_address,
)


def test_removes_reference_prefix():

    result = clean_reference_address(
        "REFERENCE ENTITY, 100 Innovation Way"
    )

    assert result == "100 Innovation Way"


def test_preserves_numeric_address():

    result = clean_reference_address(
        "245 Northwind Street"
    )

    assert result == "245 Northwind Street"


def test_removes_empty_segments():

    result = clean_reference_address(
        "ENTITY, , 800 Cloud Road, "
    )

    assert result == "800 Cloud Road"


def test_handles_none():

    assert clean_reference_address(
        None
    ) == ""


def test_collapses_repeated_spaces():

    result = clean_reference_address(
        "ENTITY, 55   Analytics Avenue"
    )

    assert result == "55 Analytics Avenue"
