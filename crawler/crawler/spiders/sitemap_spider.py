import scrapy
from crawler.items import ArticleURLItem


class SitemapSpider(scrapy.Spider):
    name = "sitemap"

    allowed_domains = ["ethiopianmonitor.com"]

    start_urls = [
        "https://ethiopianmonitor.com/wp-sitemap.xml"
    ]

    def parse(self, response):
        """
        Parse the main WordPress sitemap and follow only article sitemaps.
        """

        # Debug: print the beginning of the XML response
        self.logger.info("===== START OF SITEMAP RESPONSE =====")
        self.logger.info(response.text[:1000])
        self.logger.info("===== END OF PREVIEW =====")

        # Namespace-safe XPath
        sitemap_urls = response.xpath(
            "//*[local-name()='loc']/text()"
        ).getall()

        self.logger.info(f"Found {len(sitemap_urls)} sitemap(s).")

        for sitemap_url in sitemap_urls:

            self.logger.info(f"Sitemap: {sitemap_url}")

            if "posts-post" in sitemap_url:

                yield scrapy.Request(
                    url=sitemap_url,
                    callback=self.parse_post_sitemap
                )

    def parse_post_sitemap(self, response):
        """
        Extract article URLs from each post sitemap.
        """

        article_urls = response.xpath(
            "//*[local-name()='loc']/text()"
        ).getall()

        self.logger.info(
            f"Found {len(article_urls)} article URLs."
        )

        for article_url in article_urls:

            yield ArticleURLItem(
                url=article_url,
                source="Ethiopian Monitor"
            )