from pathlib import Path
import pandas as pd

from database.schemas import ArticleSchema


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "ethiopian_monitor_articles_clean.csv"
)


def test_all_articles_pass_pydantic_validation():

    df = pd.read_csv(DATA_FILE)

    validation_errors = []

    for index, row in df.iterrows():

        try:

            ArticleSchema(
                **row.to_dict()
            )

        except Exception as error:

            validation_errors.append(
                {
                    "row": index,
                    "error": str(error)
                }
            )

    assert validation_errors == []