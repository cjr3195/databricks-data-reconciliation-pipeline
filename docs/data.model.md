# Synthetic Data Model

All datasets in this project are synthetic and were designed
specifically to demonstrate reconciliation and data-quality patterns.

No production data or proprietary identifiers are included.

## Data Flow

```mermaid
flowchart LR
    A[Weekly Accounts Report] --> B[Account Extraction]
    B --> C[Account Universe]
    C --> D[Identifier Extraction]
    D --> E[Identifier Registry]
    E --> F[Address Cleaning]
    F --> G[Enrichment]
    G --> H[Address Matching]
    H --> I[Business Rules]
    I --> J[Audit]
    J --> K[Final Excel Report]
```

## Source Model

```mermaid
erDiagram
    WEEKLY_ACCOUNT {
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
        string parent_contract
    }

    IDENTIFIER_REGISTRY {
        string identifier PK
        string identifier_type
        string status
        string entity_name
        string raw_address
    }

    WEEKLY_ACCOUNT ||--o| ACCOUNT_UNIVERSE : reconciles_to
    ACCOUNT_UNIVERSE ||--o{ IDENTIFIER_REGISTRY : references
```

## Synthetic Scenarios

The sample data intentionally includes:

- exact identifier matches
- missing identifiers
- multiple identifiers
- inactive identifiers
- address abbreviation differences
- address prefixes requiring cleaning
- ended accounts
- special account categories
- unresolved cases requiring manual review
