from pathlib import Path
import pandas as pd


# Project root
BASE_DIR = Path(__file__).resolve().parents[1]

# Cleaned dataset
DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "ethiopian_monitor_articles_clean.csv"
)


def load_data():
    """Load the cleaned article dataset."""
    assert DATA_FILE.exists(), (
        f"Dataset not found: {DATA_FILE}"
    )

    return pd.read_csv(DATA_FILE)


def test_dataset_exists():
    """Verify the cleaned dataset exists."""
    assert DATA_FILE.exists()


def test_record_count():
    """Verify the expected number of articles."""
    df = load_data()

    assert len(df) == 7823


def test_required_columns():
    """Verify all required columns exist."""

    df = load_data()

    required_columns = [
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

    for column in required_columns:
        assert column in df.columns


def test_no_duplicate_urls():
    """Verify article URLs are unique."""

    df = load_data()

    duplicate_urls = df["article_url"].duplicated().sum()

    assert duplicate_urls == 0


def test_no_empty_content():
    """Verify articles have content."""

    df = load_data()

    empty_content = (
        df["content"]
        .fillna("")
        .str.strip()
        .eq("")
        .sum()
    )

    assert empty_content == 0


def test_no_missing_required_fields():
    """Verify required fields have no missing values."""

    df = load_data()

    required_columns = [
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

    missing_values = df[required_columns].isna().sum().sum()

    assert missing_values == 0


def test_word_count_is_valid():
    """Verify word counts are positive."""

    df = load_data()

    assert (df["word_count"] > 0).all()


def test_word_count_matches_content():
    """Verify stored word counts match article content."""

    df = load_data()

    calculated_counts = (
        df["content"]
        .str.split()
        .str.len()
    )

    assert (
        calculated_counts
        == df["word_count"]
    ).all()