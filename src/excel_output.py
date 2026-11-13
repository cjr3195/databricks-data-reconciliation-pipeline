from datetime import datetime
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import (
    Alignment,
    Font,
    PatternFill,
)
from openpyxl.utils import (
    get_column_letter,
)


SHEET_RESULTS = "Account Results"
SHEET_IDENTIFIER_AUDIT = "Identifier Audit"
SHEET_AUDIT_SUMMARY = "Audit Summary"
SHEET_QUALITY = "Quality Gates"
SHEET_RUN_SUMMARY = "Run Summary"


def _format_sheet(
    worksheet,
) -> None:
    """
    Apply lightweight analyst-facing formatting.
    """

    header_fill = PatternFill(
        fill_type="solid",
        fgColor="1F4E78",
    )

    header_font = Font(
        color="FFFFFF",
        bold=True,
    )

    header_alignment = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True,
    )

    for cell in worksheet[1]:

        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = (
            header_alignment
        )

    worksheet.freeze_panes = "A2"

    if (
        worksheet.max_row >= 1
        and worksheet.max_column >= 1
    ):
        worksheet.auto_filter.ref = (
            worksheet.dimensions
        )

    sample_rows = min(
        worksheet.max_row,
        200,
    )

    for column_index in range(
        1,
        worksheet.max_column + 1,
    ):

        values = []

        for row_index in range(
            1,
            sample_rows + 1,
        ):

            value = worksheet.cell(
                row=row_index,
                column=column_index,
            ).value

            if value is not None:
                values.append(
                    len(str(value))
                )

        width = (
            max(values) + 2
            if values
            else 10
        )

        width = min(
            max(width, 10),
            40,
        )

        worksheet.column_dimensions[
            get_column_letter(
                column_index
            )
        ].width = width


def _create_run_summary(
    pipeline_result: dict,
) -> pd.DataFrame:

    run_data = {
        "generated_at":
            datetime.now()
            .isoformat(
                timespec="seconds"
            ),

        "status":
            pipeline_result[
                "status"
            ],

        "organizations":
            pipeline_result[
                "organizations"
            ],

        "professionals":
            pipeline_result[
                "professionals"
            ],

        "accounts":
            pipeline_result[
                "accounts"
            ],

        "universe_matches":
            pipeline_result[
                "universe_matches"
            ],

        "identifiers":
            pipeline_result[
                "identifiers"
            ],

        "identifier_matches":
            pipeline_result[
                "identifier_matches"
            ],

        "address_matches":
            pipeline_result[
                "address_matches"
            ],

        "manual_review":
            pipeline_result[
                "manual_review"
            ],

        "quality_status":
            pipeline_result[
                "quality_status"
            ],

        "quality_checks":
            pipeline_result[
                "quality_checks"
            ],

        "failed_checks":
            pipeline_result[
                "failed_checks"
            ],
    }

    return pd.DataFrame(
        [run_data]
    )


def export_reconciliation_report(
    pipeline_result: dict,
    output_path: Path,
) -> dict:
    """
    Generate and validate the portfolio Excel report.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results = (
        pipeline_result[
            "results"
        ].copy()
    )

    identifier_audit = (
        pipeline_result[
            "identifier_audit"
        ].copy()
    )

    audit_summary = (
        pipeline_result[
            "audit_summary"
        ].copy()
    )

    quality_details = (
        pipeline_result[
            "quality_details"
        ].copy()
    )

    run_summary = (
        _create_run_summary(
            pipeline_result
        )
    )

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl",
    ) as writer:

        results.to_excel(
            writer,
            sheet_name=SHEET_RESULTS,
            index=False,
        )

        identifier_audit.to_excel(
            writer,
            sheet_name=(
                SHEET_IDENTIFIER_AUDIT
            ),
            index=False,
        )

        audit_summary.to_excel(
            writer,
            sheet_name=(
                SHEET_AUDIT_SUMMARY
            ),
            index=False,
        )

        quality_details.to_excel(
            writer,
            sheet_name=SHEET_QUALITY,
            index=False,
        )

        run_summary.to_excel(
            writer,
            sheet_name=(
                SHEET_RUN_SUMMARY
            ),
            index=False,
        )

    workbook = load_workbook(
        output_path
    )

    for worksheet in workbook.worksheets:
        _format_sheet(
            worksheet
        )

    workbook.save(
        output_path
    )

    workbook.close()

    return validate_excel_output(
        output_path=output_path,
        expected_account_rows=len(
            results
        ),
    )


def validate_excel_output(
    output_path: Path,
    expected_account_rows: int,
) -> dict:

    if not output_path.exists():
        raise FileNotFoundError(
            "Excel output was not created."
        )

    if output_path.stat().st_size == 0:
        raise ValueError(
            "Excel output is empty."
        )

    workbook = load_workbook(
        output_path,
        read_only=True,
        data_only=False,
    )

    required_sheets = {
        SHEET_RESULTS,
        SHEET_IDENTIFIER_AUDIT,
        SHEET_AUDIT_SUMMARY,
        SHEET_QUALITY,
        SHEET_RUN_SUMMARY,
    }

    actual_sheets = set(
        workbook.sheetnames
    )

    missing_sheets = (
        required_sheets
        - actual_sheets
    )

    if missing_sheets:

        workbook.close()

        raise ValueError(
            "Excel output is missing sheets: "
            + ", ".join(
                sorted(missing_sheets)
            )
        )

    actual_account_rows = (
        workbook[
            SHEET_RESULTS
        ].max_row - 1
    )

    workbook.close()

    if (
        actual_account_rows
        != expected_account_rows
    ):
        raise ValueError(
            "Excel Account Results row count "
            "does not reconcile. "
            f"Expected: {expected_account_rows}. "
            f"Actual: {actual_account_rows}."
        )

    return {
        "output_file":
            str(output_path),

        "file_size_bytes":
            output_path.stat().st_size,

        "sheet_count":
            len(actual_sheets),

        "account_rows":
            actual_account_rows,

        "status":
            "VALID",
    }
