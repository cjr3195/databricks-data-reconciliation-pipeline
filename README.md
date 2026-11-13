# Databricks Data Reconciliation Pipeline

A production-style data engineering project demonstrating how a
legacy spreadsheet-driven reconciliation workflow can be modernized
into a modular Python and Databricks pipeline.

The project focuses on deterministic transformations, reference-data
reconciliation, address matching, business rules, auditability,
quality gates, and automated Excel delivery.

> **Portfolio-safe project:** all datasets, organizations, people,
> identifiers, addresses, and scenarios in this repository are
> synthetic.

---

## Architecture

```mermaid
flowchart LR
    A["Weekly Account Report"] --> B["Input Validation"]
    B --> C["Account Universe"]
    C --> D["Identifier Extraction"]
    D --> E["Identifier Registry"]
    E --> F["Address Cleaning"]
    F --> G["Data Enrichment"]
    G --> H["Address Matching"]
    H --> I["Business Rules"]
    I --> J["Audit Layer"]
    J --> K["Quality Gates"]
    K --> L["Excel Output"]
```

---

## Modernization Journey

```mermaid
flowchart LR
    A["Spreadsheet Workflow"] --> B["Python Automation"]
    B --> C["Modular Pipeline"]
    C --> D["PySpark Processing"]
    D --> E["Databricks Job"]
    E --> F["Auditable Output"]
```

The objective is not merely to automate Excel operations. The
workflow is redesigned so that the spreadsheet becomes a delivery
artifact rather than the execution engine.

---

## Synthetic Data Model

```mermaid
erDiagram
    WEEKLY_ACCOUNT {
        string scenario_id
        string account_id PK
        string account_name
        string current_identifier
        string address
        string account_type
        string status
    }

    ACCOUNT_UNIVERSE {
        string account_id PK
        string primary_identifier
        string secondary_identifier
        string identifier_status
        string canonical_address
        string account_category
        string account_end_status
        date last_activity_date
        string distribution_method
        string parent_contract
    }

    IDENTIFIER_REGISTRY {
        string identifier PK
        string identifier_type
        string status
        string entity_name
        string raw_address
        string city
        string state
        string postal_code
    }

    WEEKLY_ACCOUNT ||--o| ACCOUNT_UNIVERSE : reconciles_to
    ACCOUNT_UNIVERSE ||--o{ IDENTIFIER_REGISTRY : references
```

---

## Demonstrated Scenarios

The synthetic dataset intentionally contains controlled cases rather
than randomly generated rows.

| Scenario | Engineering behavior |
|---|---|
| Exact match | Full reconciliation |
| Address abbreviation | STREET/ST and ROAD/RD equivalence |
| Address prefix | Reference-address cleanup |
| Missing primary identifier | Partial reconciliation |
| Missing secondary identifier | Partial reconciliation |
| Missing identifiers | Manual-review exception |
| Inactive identifier | Status-aware validation |
| Ended account | Business-rule outcome |
| Special account category | No-action rule |
| Multiple identifiers | One-to-many identifier extraction |
| Unresolved exception | Analyst review |

---

## Pipeline Design

```mermaid
flowchart TD
    INPUT["Synthetic Input Workbook"]
    UNIVERSE["Account Universe"]
    IDS["Identifier Extraction"]
    REGISTRY["Identifier Registry"]
    CLEAN["Address Cleaning"]
    ENRICH["Enrichment"]
    MATCH["Address Matching"]
    RULES["Business Rules"]
    AUDIT["Audit"]
    QG["Quality Gates"]
    OUTPUT["Excel Report"]

    INPUT --> UNIVERSE
    UNIVERSE --> IDS
    IDS --> REGISTRY
    REGISTRY --> CLEAN
    CLEAN --> ENRICH
    ENRICH --> MATCH
    MATCH --> RULES
    RULES --> AUDIT
    AUDIT --> QG
    QG --> OUTPUT
```

---

## Quality Engineering

The project will implement deterministic quality gates throughout the
pipeline.

```mermaid
flowchart TD
    A["Input Valid"] --> B["Required Sheets"]
    B --> C["Accounts Extracted"]
    C --> D["Universe Reconciled"]
    D --> E["Identifiers Extracted"]
    E --> F["Registry Reconciled"]
    F --> G["Rows Preserved"]
    G --> H["Address Flags Valid"]
    H --> I["Rules Reconciled"]
    I --> J["Audit Reconciled"]
    J --> K["Excel Generated"]
    K --> L["Final Artifact Valid"]
```

Failures should identify the pipeline stage where reconciliation
broke rather than silently producing an incomplete report.

---

## Repository Structure

```text
databricks-data-reconciliation-pipeline/
│
├── data/
│   ├── input/
│   ├── reference/
│   └── expected/
│
├── scripts/
│   └── generate_synthetic_data.py
│
├── src/
│   ├── ingestion.py
│   ├── universe.py
│   ├── identifiers.py
│   ├── reference_lookup.py
│   ├── address_cleaning.py
│   ├── enrichment.py
│   ├── address_matching.py
│   ├── business_rules.py
│   ├── audit.py
│   ├── excel_output.py
│   └── pipeline.py
│
├── tests/
├── notebooks/
├── docs/
└── output/
```

---

## Technology Stack

- Python
- pandas
- PySpark
- Databricks
- openpyxl
- pytest
- GitHub

---

## Current Status

- [x] Repository structure
- [x] Synthetic data model
- [x] Controlled reconciliation scenarios
- [x] Synthetic data generator
- [ ] Modular pipeline
- [ ] Automated quality gates
- [ ] Excel reporting
- [ ] Databricks workflow demo
- [ ] Portfolio case study

---

## Data Privacy

This repository does **not** contain production code, proprietary
table names, credentials, customer records, real healthcare
identifiers, internal company documentation, or production outputs.

Identifier formats such as `PRI-A001` and `SEC-H001` are deliberately
fictional and have no relationship to real-world healthcare
identifiers.
