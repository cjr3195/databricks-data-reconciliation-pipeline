# Databricks notebook source

"""
Portfolio-safe Databricks entrypoint for the
Data Reconciliation Pipeline.

All data used by this demo is synthetic.
"""

from pathlib import Path

from src.pipeline import run_pipeline


# =========================================================
# JOB PARAMETERS
# =========================================================

try:
    dbutils.widgets.text(
        "environment",
        "demo",
        "Environment",
    )

    environment = (
        dbutils.widgets.get(
            "environment"
        )
    )

except NameError:
    environment = "local"


# =========================================================
# RUN PIPELINE
# =========================================================

result = run_pipeline()


# =========================================================
# JOB RESULT
# =========================================================

job_result = {
    "environment":
        environment,

    "status":
        result["status"],

    "accounts":
        result["accounts"],

    "organizations":
        result["organizations"],

    "professionals":
        result["professionals"],

    "universe_matches":
        result["universe_matches"],

    "identifiers":
        result["identifiers"],

    "identifier_matches":
        result["identifier_matches"],

    "address_matches":
        result["address_matches"],

    "manual_review":
        result["manual_review"],

    "quality_status":
        result["quality_status"],

    "quality_checks":
        result["quality_checks"],

    "failed_checks":
        result["failed_checks"],

    "output_file":
        result["output"][
            "output_file"
        ],
}


if result["status"] != "SUCCESS":
    raise RuntimeError(
        "Reconciliation pipeline failed."
    )


if result["failed_checks"] != 0:
    raise RuntimeError(
        "One or more quality gates failed."
    )


job_result
