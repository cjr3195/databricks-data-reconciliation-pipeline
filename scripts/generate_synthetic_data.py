from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT_DIR = ROOT / "data" / "input"
REFERENCE_DIR = ROOT / "data" / "reference"
EXPECTED_DIR = ROOT / "data" / "expected"

for directory in [
    INPUT_DIR,
    REFERENCE_DIR,
    EXPECTED_DIR,
]:
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


organizations = [
    {
        "scenario_id": "S01",
        "account_id": "ORG-1001",
        "account_name": "Northwind Community Center",
        "current_identifier": "PRI-A001",
        "address": "100 Innovation Way",
        "city": "Seattle",
        "state": "WA",
        "postal_code": "98101",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S02",
        "account_id": "ORG-1002",
        "account_name": "Contoso Specialty Clinic",
        "current_identifier": "PRI-A002",
        "address": "245 Northwind Street",
        "city": "Austin",
        "state": "TX",
        "postal_code": "78701",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S03",
        "account_id": "ORG-1003",
        "account_name": "Fabrikam Regional Center",
        "current_identifier": "PRI-A003",
        "address": "800 Cloud Road",
        "city": "Denver",
        "state": "CO",
        "postal_code": "80202",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S04",
        "account_id": "ORG-1004",
        "account_name": "Adventure Works Medical Group",
        "current_identifier": "PRI-A004",
        "address": "55 Analytics Avenue",
        "city": "Miami",
        "state": "FL",
        "postal_code": "33101",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S05",
        "account_id": "ORG-1005",
        "account_name": "Blue Yonder Wellness Center",
        "current_identifier": "PRI-A005",
        "address": "720 Lakeview Boulevard",
        "city": "Chicago",
        "state": "IL",
        "postal_code": "60601",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S06",
        "account_id": "ORG-1006",
        "account_name": "Woodgrove Care Network",
        "current_identifier": "PRI-A006",
        "address": "310 Data Drive",
        "city": "Phoenix",
        "state": "AZ",
        "postal_code": "85001",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S07",
        "account_id": "ORG-1007",
        "account_name": "Alpine Health Services",
        "current_identifier": "PRI-A007",
        "address": "410 Summit Lane",
        "city": "Portland",
        "state": "OR",
        "postal_code": "97201",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S09",
        "account_id": "ORG-1009",
        "account_name": "Fourth Coffee Community Clinic",
        "current_identifier": "PRI-A009",
        "address": "900 Legacy Court",
        "city": "Boston",
        "state": "MA",
        "postal_code": "02108",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S10",
        "account_id": "ORG-1010",
        "account_name": "Tailspin Health Group",
        "current_identifier": "PRI-A010",
        "address": "88 Community Place",
        "city": "Atlanta",
        "state": "GA",
        "postal_code": "30301",
        "account_type": "SPECIAL",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S11",
        "account_id": "ORG-1011",
        "account_name": "Litware Regional Services",
        "current_identifier": "PRI-A011",
        "address": "120 Multiple Ave",
        "city": "Nashville",
        "state": "TN",
        "postal_code": "37201",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
]


professionals = [
    {
        "scenario_id": "S01",
        "account_id": "PRO-2001",
        "account_name": "Alex Morgan",
        "current_identifier": "PRI-P001",
        "address": "100 Innovation Way",
        "city": "Seattle",
        "state": "WA",
        "postal_code": "98101",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S02",
        "account_id": "PRO-2002",
        "account_name": "Taylor Quinn",
        "current_identifier": "PRI-P002",
        "address": "245 Northwind St",
        "city": "Austin",
        "state": "TX",
        "postal_code": "78701",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S04",
        "account_id": "PRO-2004",
        "account_name": "Jordan Reed",
        "current_identifier": "PRI-P004",
        "address": "55 Analytics Ave",
        "city": "Miami",
        "state": "FL",
        "postal_code": "33101",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S06",
        "account_id": "PRO-2006",
        "account_name": "Casey Blake",
        "current_identifier": "PRI-P006",
        "address": "310 Data Dr",
        "city": "Phoenix",
        "state": "AZ",
        "postal_code": "85001",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S08",
        "account_id": "PRO-2008",
        "account_name": "Morgan Ellis",
        "current_identifier": "PRI-P008",
        "address": "700 Archive Road",
        "city": "Raleigh",
        "state": "NC",
        "postal_code": "27601",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S10",
        "account_id": "PRO-2010",
        "account_name": "Riley Morgan",
        "current_identifier": "PRI-P010",
        "address": "88 Community Pl",
        "city": "Atlanta",
        "state": "GA",
        "postal_code": "30301",
        "account_type": "SPECIAL",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S11",
        "account_id": "PRO-2011",
        "account_name": "Avery Brooks",
        "current_identifier": "PRI-P011",
        "address": "120 Multiple Avenue",
        "city": "Nashville",
        "state": "TN",
        "postal_code": "37201",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
    {
        "scenario_id": "S12",
        "account_id": "PRO-2012",
        "account_name": "Cameron Lee",
        "current_identifier": "PRI-P012",
        "address": "999 Review Drive",
        "city": "Dallas",
        "state": "TX",
        "postal_code": "75201",
        "account_type": "STANDARD",
        "status": "ACTIVE",
    },
]


universe = [
    {
        "account_id": row["account_id"],
        "account_name": row["account_name"],
        "primary_identifier": (
            f"PRI-U{index:03d}"
        ),
        "secondary_identifier": (
            f"SEC-H{index:03d}"
        ),
        "identifier_status": "ACTIVE",
        "canonical_address": row["address"],
        "account_category": row["account_type"],
        "account_end_status": "ACTIVE",
        "last_activity_date": "2026-10-31",
        "distribution_method": "DIRECT",
        "parent_contract": (
            f"Synthetic Contract {index:02d}"
        ),
    }
    for index, row in enumerate(
        organizations + professionals,
        start=1,
    )
]

# Controlled scenarios
for row in universe:
    if row["account_id"] == "ORG-1009":
        row["account_end_status"] = "ENDED"

    if row["account_id"] == "PRO-2008":
        row["identifier_status"] = "INACTIVE"

    if row["account_id"] == "ORG-1011":
        row["primary_identifier"] = (
            "PRI-U011;PRI-U111"
        )

    if row["account_id"] == "PRO-2011":
        row["secondary_identifier"] = (
            "SEC-H017;SEC-H117"
        )


registry = []

for row in universe:
    primary_values = (
        row["primary_identifier"]
        .split(";")
    )

    secondary_values = (
        row["secondary_identifier"]
        .split(";")
    )

    for identifier in primary_values:
        registry.append({
            "identifier": identifier,
            "identifier_type": "PRIMARY",
            "status": "ACTIVE",
            "entity_name": row["account_name"],
            "raw_address": (
                f"REFERENCE ENTITY, "
                f"{row['canonical_address']}"
            ),
            "city": "",
            "state": "",
            "postal_code": "",
        })

    for identifier in secondary_values:
        registry.append({
            "identifier": identifier,
            "identifier_type": "SECONDARY",
            "status": (
                "INACTIVE"
                if row["account_id"] == "PRO-2008"
                else "ACTIVE"
            ),
            "entity_name": row["account_name"],
            "raw_address": row["canonical_address"],
            "city": "",
            "state": "",
            "postal_code": "",
        })


# Deliberately remove identifiers for missing-reference scenarios.
registry = [
    row
    for row in registry
    if row["identifier"]
    not in {
        "SEC-H005",
        "PRI-U006",
        "PRI-U007",
        "SEC-H007",
    }
]


expectations = [
    {
        "scenario_id": "S01",
        "scenario": "Exact match",
        "expected_outcome": "RESOLVED",
    },
    {
        "scenario_id": "S02",
        "scenario": "Street abbreviation",
        "expected_outcome": "RESOLVED",
    },
    {
        "scenario_id": "S03",
        "scenario": "Road abbreviation",
        "expected_outcome": "RESOLVED",
    },
    {
        "scenario_id": "S04",
        "scenario": "Address prefix cleanup",
        "expected_outcome": "RESOLVED",
    },
    {
        "scenario_id": "S05",
        "scenario": "Secondary identifier missing",
        "expected_outcome": "PARTIAL_MATCH",
    },
    {
        "scenario_id": "S06",
        "scenario": "Primary identifier missing",
        "expected_outcome": "PARTIAL_MATCH",
    },
    {
        "scenario_id": "S07",
        "scenario": "No identifiers found",
        "expected_outcome": "MANUAL_REVIEW",
    },
    {
        "scenario_id": "S08",
        "scenario": "Inactive secondary identifier",
        "expected_outcome": "MANUAL_REVIEW",
    },
    {
        "scenario_id": "S09",
        "scenario": "Ended account",
        "expected_outcome": "ACCOUNT_ENDED",
    },
    {
        "scenario_id": "S10",
        "scenario": "Special account category",
        "expected_outcome": "NO_ACTION",
    },
    {
        "scenario_id": "S11",
        "scenario": "Multiple identifiers",
        "expected_outcome": "RESOLVED",
    },
    {
        "scenario_id": "S12",
        "scenario": "Unresolved exception",
        "expected_outcome": "MANUAL_REVIEW",
    },
]


organizations_df = pd.DataFrame(
    organizations
)

professionals_df = pd.DataFrame(
    professionals
)

universe_df = pd.DataFrame(
    universe
)

registry_df = pd.DataFrame(
    registry
)

expectations_df = pd.DataFrame(
    expectations
)


with pd.ExcelWriter(
    INPUT_DIR / "weekly_accounts_report.xlsx",
    engine="openpyxl",
) as writer:

    organizations_df.to_excel(
        writer,
        sheet_name="ORGANIZATIONS",
        index=False,
    )

    professionals_df.to_excel(
        writer,
        sheet_name="PROFESSIONALS",
        index=False,
    )


universe_df.to_csv(
    REFERENCE_DIR / "account_universe.csv",
    index=False,
)

registry_df.to_csv(
    REFERENCE_DIR / "identifier_registry.csv",
    index=False,
)

expectations_df.to_csv(
    EXPECTED_DIR / "scenario_expectations.csv",
    index=False,
)


print("Synthetic portfolio datasets created.")
