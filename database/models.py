from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    Index,
)

from database.database import Base


class Article(Base):

    __tablename__ = "articles"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    source = Column(
        String(100),
        nullable=False
    )

    article_url = Column(
        Text,
        nullable=False,
        unique=True
    )

    title = Column(
        Text,
        nullable=False
    )

    author = Column(
        String(255),
        nullable=False
    )

    published_date = Column(
        DateTime(timezone=True),
        nullable=False
    )

    category = Column(
        String(255),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    language = Column(
        String(50),
        nullable=False
    )

    word_count = Column(
        Integer,
        nullable=False
    )

    scraped_at = Column(
        DateTime,
        nullable=False
    )


# Additional indexes for faster searches

Index(
    "idx_articles_published_date",
    Article.published_date
)

Index(
    "idx_articles_category",
    Article.category
)

Index(
    "idx_articles_source",
    Article.source
)