import pandas as pd
from pathlib import Path

from database.schemas import ArticleSchema


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "ethiopian_monitor_articles_clean.csv"
)

VALIDATION_DIR = (
    BASE_DIR
    / "data"
    / "validation"
)

VALID_FILE = (
    VALIDATION_DIR
    / "valid_articles.csv"
)

INVALID_FILE = (
    VALIDATION_DIR
    / "invalid_articles.csv"
)


# Create validation directory
VALIDATION_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("PYDANTIC DATA VALIDATION")
print("=" * 60)

print("\nReading dataset:")
print(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

print(
    f"\nTotal records loaded: {len(df)}"
)


# ============================================================
# VALIDATION
# ============================================================

valid_records = []
invalid_records = []

for index, row in df.iterrows():

    try:

        article = ArticleSchema(
            **row.to_dict()
        )

        valid_records.append(
            article.model_dump()
        )

    except Exception as e:

        invalid_records.append({
            "row_number": index,
            "error": str(e),
            **row.to_dict()
        })


# ============================================================
# RESULTS
# ============================================================

valid_df = pd.DataFrame(
    valid_records
)

invalid_df = pd.DataFrame(
    invalid_records
)


print("\n" + "=" * 60)
print("VALIDATION RESULTS")
print("=" * 60)

print(
    f"\nTotal records: {len(df)}"
)

print(
    f"Valid records: {len(valid_df)}"
)

print(
    f"Invalid records: {len(invalid_df)}"
)


# ============================================================
# SAVE VALID RECORDS
# ============================================================

valid_df.to_csv(
    VALID_FILE,
    index=False
)

print(
    f"\nValid records saved to:"
)

print(
    VALID_FILE
)


# ============================================================
# SAVE INVALID RECORDS
# ============================================================

if len(invalid_df) > 0:

    invalid_df.to_csv(
        INVALID_FILE,
        index=False
    )

    print(
        "\nInvalid records saved to:"
    )

    print(
        INVALID_FILE
    )

else:

    print(
        "\nNo invalid records found."
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)