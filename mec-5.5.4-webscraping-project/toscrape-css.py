import scrapy


class QuotesSpider(scrapy.Spider):
        name = "toscrape-css"
#Method 2-faster way- no start_requests needed.

        start_urls =['http://quotes.toscrape.com/']
        
        def parse(self, response):
            for quote in response.css("div.quote"):
               yield {
                    'text': quote.css('span.text::text').get(),
                    'author': quote.css('small.author::text').get(),
                    'tags': quote.css('div.tags a.tag::text').getall(),
                } 

            for href in response.css('ul.pager a::attr(href)'):
               yield response.follow(href, callback=self.parse) 