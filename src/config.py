from pathlib import Path


PROJECT_ROOT = (
    Path(__file__).resolve().parents[1]
)

DATA_DIR = PROJECT_ROOT / "data"

INPUT_DIR = DATA_DIR / "input"
REFERENCE_DIR = DATA_DIR / "reference"
EXPECTED_DIR = DATA_DIR / "expected"
OUTPUT_DIR = PROJECT_ROOT / "output"


INPUT_FILE = (
    INPUT_DIR
    / "weekly_accounts_report.xlsx"
)

UNIVERSE_FILE = (
    REFERENCE_DIR
    / "account_universe.csv"
)

REGISTRY_FILE = (
    REFERENCE_DIR
    / "identifier_registry.csv"
)

EXPECTATIONS_FILE = (
    EXPECTED_DIR
    / "scenario_expectations.csv"
)


ORGANIZATIONS_SHEET = "ORGANIZATIONS"
PROFESSIONALS_SHEET = "PROFESSIONALS"


PRIMARY_IDENTIFIER = "PRIMARY"
SECONDARY_IDENTIFIER = "SECONDARY"


ADDRESS_MATCH_THRESHOLD = 0.75
