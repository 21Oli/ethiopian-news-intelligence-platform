import scrapy
import pandas as pd
from datetime import datetime

from crawler.items import ArticleItem


class ArticleSpider(scrapy.Spider):

    name = "articles"

    allowed_domains = [
        "ethiopianmonitor.com"
    ]

    async def start(self):

        # -----------------------------------
        # CSV FILE PATH
        # -----------------------------------

        csv_path = "../data/urls/article_urls.csv"

        self.logger.info("=" * 60)
        self.logger.info("ARTICLE SPIDER STARTED")
        self.logger.info(f"Reading CSV: {csv_path}")
        self.logger.info("=" * 60)

        # -----------------------------------
        # READ ARTICLE URLS
        # -----------------------------------

        try:
            df = pd.read_csv(csv_path)

        except Exception as e:
            self.logger.error(
                f"Could not read CSV file: {e}"
            )
            return

        self.logger.info(
            f"Total URLs found: {len(df)}"
        )

        # -----------------------------------
        # REMOVE MISSING URLS
        # -----------------------------------

        df = df.dropna(
            subset=["url"]
        )

        # -----------------------------------
        # REMOVE DUPLICATE URLS
        # -----------------------------------

        df = df.drop_duplicates(
            subset=["url"]
        )

        self.logger.info(
            f"Unique URLs to scrape: {len(df)}"
        )

        # -----------------------------------
        # TEST MODE
        # -----------------------------------
        # Change to True to test 5 articles
        # Change to False to scrape everything

        TEST_MODE = False

        if TEST_MODE:

            df = df.head(5)

            self.logger.info(
                f"TEST MODE ENABLED: "
                f"Scraping {len(df)} articles"
            )

        else:

            self.logger.info(
                f"FULL MODE ENABLED: "
                f"Scraping {len(df)} articles"
            )

        # -----------------------------------
        # SEND REQUESTS
        # -----------------------------------

        for url in df["url"]:

            self.logger.info(
                f"Sending request: {url}"
            )

            yield scrapy.Request(

                url=url,

                callback=self.parse,

                errback=self.handle_error,

                dont_filter=True
            )

    def parse(self, response):

        self.logger.info(
            f"SUCCESS: {response.url}"
        )

        # -----------------------------------
        # TITLE
        # -----------------------------------

        title = response.css(
            "h1.cm-entry-title::text"
        ).get()

        if title:
            title = title.strip()

        # -----------------------------------
        # AUTHOR
        # -----------------------------------

        author = response.css(
            ".url.fn.n::text"
        ).get()

        if author:
            author = author.strip()

        # -----------------------------------
        # PUBLISHED DATE
        # -----------------------------------

        published_date = response.css(
            "time::attr(datetime)"
        ).get()

        # -----------------------------------
        # CATEGORY
        # -----------------------------------

        category = response.css(
            "a[href*='/category/']::text"
        ).get()

        if category:
            category = category.strip()

        # -----------------------------------
        # FEATURED IMAGE
        # -----------------------------------

        featured_image = response.css(
            ".cm-entry-summary img::attr(src)"
        ).get()

        # -----------------------------------
        # TAGS
        # -----------------------------------

        tags = response.css(
            "a[href*='/tag/']::text"
        ).getall()

        tags = [
            tag.strip()
            for tag in tags
            if tag.strip()
        ]

        # -----------------------------------
        # ARTICLE CONTENT
        # -----------------------------------

        paragraphs = response.css(
            ".cm-entry-summary p *::text, "
            ".cm-entry-summary p::text"
        ).getall()

        content = "\n".join(

            p.strip()

            for p in paragraphs

            if p.strip()

        )

        # -----------------------------------
        # WORD COUNT
        # -----------------------------------

        word_count = len(
            content.split()
        )

        # -----------------------------------
        # LANGUAGE
        # -----------------------------------

        language = "English"

        # -----------------------------------
        # SCRAPED TIME
        # -----------------------------------

        scraped_at = datetime.now().isoformat()

        # -----------------------------------
        # LOG EXTRACTION RESULTS
        # -----------------------------------

        self.logger.info(
            f"Title: {title}"
        )

        self.logger.info(
            f"Word count: {word_count}"
        )

        # -----------------------------------
        # SAVE ARTICLE
        # -----------------------------------

        yield ArticleItem(

            source="Ethiopian Monitor",

            article_url=response.url,

            title=title,

            author=author,

            published_date=published_date,

            category=category,

            content=content,

            featured_image=featured_image,

            tags=tags,

            language=language,

            word_count=word_count,

            scraped_at=scraped_at

        )

    # -----------------------------------
    # ERROR HANDLING
    # -----------------------------------

    def handle_error(self, failure):

        request = failure.request

        self.logger.error(
            f"REQUEST FAILED: {request.url}"
        )

        self.logger.error(
            repr(failure)
        )