import pandas as pd
from sqlalchemy import text

from database.connection import engine


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/processed/ethiopian_monitor_articles_clean.csv"


# ============================================================
# INSERT DATA
# ============================================================

def insert_articles():

    print("=" * 60)
    print("INSERTING ARTICLES INTO POSTGRESQL")
    print("=" * 60)

    print("\nReading validated dataset:")
    print(INPUT_FILE)

    # Read cleaned and validated CSV
    df = pd.read_csv(INPUT_FILE)

    print(f"Records loaded: {len(df)}")

    # Select only database columns
    df = df[
        [
            "source",
            "article_url",
            "title",
            "author",
            "published_date",
            "category",
            "content",
            "language",
            "word_count",
            "scraped_at",
        ]
    ]

    print("\nInserting records into PostgreSQL...")

    # Insert data
    df.to_sql(
        "articles",
        con=engine,
        schema="public",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500,
    )

    print("\nData insertion completed successfully!")

    # Verify count
    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT COUNT(*) FROM articles")
        )

        total_articles = result.scalar()

    print("\n" + "=" * 60)
    print("INSERTION VERIFICATION")
    print("=" * 60)

    print(f"Total articles in database: {total_articles}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    insert_articles()