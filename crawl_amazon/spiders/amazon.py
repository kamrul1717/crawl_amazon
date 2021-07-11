import scrapy
from ..items import CrawlAmazonItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = [
        'https://www.amazon.com/s?k=novel&i=stripbooks-intl-ship&ref=nb_sb_noss'
    ]

    page_number = 2

    def parse(self, response):
        items = CrawlAmazonItem()
        book_name = response.css(".a-color-base.a-text-normal::text").extract()
        book_author = response.css(".a-color-secondary .a-size-base+ .a-size-base").css('::text').extract()
        book_price = response.css(".sg-col-12-of-16:nth-child(7) .a-spacing-mini:nth-child(1) .a-price-whole , .a-spacing-top-small .a-size-mini .a-price-fraction , .a-spacing-top-small .a-size-mini .a-price-whole").css('::text').extract()
        book_image_link = response.css(".s-image::attr(src)").extract()

        items['book_name'] = book_name
        items['book_author'] = book_author
        items['book_price'] = book_price
        items['book_image_link'] = book_image_link
        yield items

        next_page = 'https://www.amazon.com/s?k=novel&i=stripbooks-intl-ship&page='+str(AmazonSpider.page_number)+'&qid=1626024295&ref=sr_pg_1'
        if AmazonSpider.page_number <= 5:
            AmazonSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)
