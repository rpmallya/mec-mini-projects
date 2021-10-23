import scrapy


class QuotesSpider(scrapy.Spider):
        name = "quotes"
#method 1- explicitally define start
        '''
        def start_requests(self):
            urls = [
                'http://quotes.toscrape.com/page/1/',
                'http://quotes.toscrape.com/page/2/',
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
        
        '''
#Method 2-faster way- no start_requests needed.

        start_urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        '''
        def parse(self, response):
            page = response.url.split("/")[-2]
            filename = 'quotes-%s.html' % page
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)
        '''
        def parse(self, response):
            for quote in response.css("div.quote"):
               yield {
                    'text': quote.css('span.text::text').get(),
                    'author': quote.css('small.author::text').get(),
                    'tags': quote.css('div.tags a.tag::text').getall(),
                } 
            '''
            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                #Long Method
                #next_page = response.urljoin(next_page)
                #yield scrapy.Request(next_page, callback=self.parse)
                
                #Short Cut
                yield response.follow(next_page,callback=self.parse)
            '''
            #instead of passing string to .follow, selector can be passed
            #for href in response.css('ul.pager a::attr(href)'):
            #   yield response.follow(href, callback=self.parse) 

            #a elements shprt cut
            #for a in response.css('ul.pager a'):
            #    yield response.follow(a, callback=self.parse)

            #createing multiple requests
            anchors=response.css('u.pager a')
            yield from response.follow_all(anchors,callback=self.parse)