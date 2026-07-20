import scrapy


class ArticleURLItem(scrapy.Item):
    """
    Stores article URLs collected from the sitemap.
    """

    # Basic information
    source = scrapy.Field()
    url = scrapy.Field()


class ArticleItem(scrapy.Item):
    """
    Stores complete article information.
    """

    source = scrapy.Field()

    article_url = scrapy.Field()

    title = scrapy.Field()

    author = scrapy.Field()

    published_date = scrapy.Field()

    category = scrapy.Field()

    content = scrapy.Field()

    featured_image = scrapy.Field()

    tags = scrapy.Field()

    language = scrapy.Field()

    word_count = scrapy.Field()

    scraped_at = scrapy.Field()