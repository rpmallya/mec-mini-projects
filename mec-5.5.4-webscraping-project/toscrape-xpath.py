import scrapy


class QuotesSpider(scrapy.Spider):
        name = "toscrape-xpath"


        start_urls =['http://quotes.toscrape.com/']
        def parse(self, response):
            for quote in response.xpath("//div[@class = \"quote\"]"): 
               yield {
                    'text': quote.xpath("//span[@class=\'text\']/text()").get(),
                    'author': quote.xpath("//small[@class=\'author\']/text()").get(),
                    'tags': quote.xpath("//div[@class=\'tags\']//a[@class=\'tag\']/text()").getall(), #quote.css('div.tags a.tag::text').getall(),
                } 
            
            next_page = response.xpath("//ul/li/a/@href").get()
            #print("------{}".format(next_page))
            if next_page is not None:
                yield response.follow(next_page,callback=self.parse)
            
            