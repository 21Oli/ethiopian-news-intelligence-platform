import pandas as pd

from database.database import SessionLocal
from database.models import Article


INPUT_FILE = (
    "data/validation/valid_articles.csv"
)


print("=" * 60)
print("LOADING VALIDATED ARTICLES")
print("=" * 60)


# ------------------------------------------------------------
# LOAD CSV
# ------------------------------------------------------------

print(
    f"\nReading dataset:\n{INPUT_FILE}"
)

df = pd.read_csv(
    INPUT_FILE
)

print(
    f"\nRecords loaded: {len(df)}"
)


# ------------------------------------------------------------
# CONVERT DATE COLUMNS
# ------------------------------------------------------------

df["published_date"] = pd.to_datetime(
    df["published_date"],
    errors="coerce",
    utc=True
)

df["scraped_at"] = pd.to_datetime(
    df["scraped_at"],
    errors="coerce"
)


# ------------------------------------------------------------
# DATABASE SESSION
# ------------------------------------------------------------

session = SessionLocal()


try:

    articles = []

    for _, row in df.iterrows():

        article = Article(

            source=row["source"],

            article_url=row["article_url"],

            title=row["title"],

            author=row["author"],

            published_date=row["published_date"],

            category=row["category"],

            content=row["content"],

            language=row["language"],

            word_count=int(
                row["word_count"]
            ),

            scraped_at=row["scraped_at"]

        )

        articles.append(article)


    print(
        f"\nInserting {len(articles)} articles..."
    )


    session.add_all(
        articles
    )

    session.commit()


    print(
        "\nSuccessfully inserted articles!"
    )

    print(
        f"Total inserted: {len(articles)}"
    )


except Exception as e:

    session.rollback()

    print(
        "\nERROR: Database insertion failed."
    )

    print(
        f"Details: {e}"
    )


finally:

    session.close()