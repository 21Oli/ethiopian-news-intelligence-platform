from datetime import datetime

from pydantic import BaseModel, HttpUrl, ConfigDict


class ArticleSchema(BaseModel):
    """
    Pydantic schema for validating Ethiopian Monitor articles.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    source: str

    article_url: HttpUrl

    title: str

    author: str

    published_date: datetime

    category: str

    content: str

    language: str

    word_count: int

    scraped_at: datetime