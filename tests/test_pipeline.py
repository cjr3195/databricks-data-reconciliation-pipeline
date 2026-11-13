from src.pipeline import (
    run_pipeline,
)


def test_pipeline_completes_successfully():

    result = run_pipeline()

    assert result["status"] == "SUCCESS"
    assert result["organizations"] == 10
    assert result["professionals"] == 8
    assert result["accounts"] == 18


def test_pipeline_passes_quality_gates():

    result = run_pipeline()

    assert (
        result["quality_status"]
        == "PASS"
    )

    assert (
        result["failed_checks"]
        == 0
    )


def test_all_accounts_reach_results():

    result = run_pipeline()

    assert len(
        result["results"]
    ) == result["accounts"]
