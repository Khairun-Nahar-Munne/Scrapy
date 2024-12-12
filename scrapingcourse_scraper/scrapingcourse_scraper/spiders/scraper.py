import scrapy


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["uk.trip.com"]
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB"]

    def parse(self, response):
            # Extract all <h3> headings
            headings = response.xpath('//h3/text()').getall()  # Using XPath

            # If you prefer CSS selectors, you can use:
            # headings = response.css('h3::text').getall()

            # Print or yield the extracted headings
            for heading in headings:
                yield {"heading": heading}