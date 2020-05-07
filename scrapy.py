import scrapy
from scrapy.loader import ItemLoader


class Escola(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()


class EscolasSpider(scrapy.Spider):

    name = 'escolaspider'
    start_urls = ['https://www.escol.as/estados']

    custom_settings = {
        'ROBOTSTXT_OBEY': False,

        'DOWNLOAD_DELAY': 0,
        'DOWNLOAD_TIMEOUT':30,
        'RANDOMIZE_DOWNLOAD_DELAY': True,

        'REACTOR_THREADPOOL_MAXSIZE': 128,
        'CONCURRENT_REQUESTS':256,
        'CONCURRENT_REQUESTS_PER_DOMAIN':256,
        'CONCURRENT_REQUESTS_PER_IP': 256,

        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY ': 0.25,
        'AUTOTHROTTLE_TARGET_CONCURRENCY' :128,
        'AUTOTHROTTLE_DEBUG' : True,

        'RETRY_ENABLED' : True,
        'RETRY_TIMES'  : 3,
        'RETRY_HTTP_CODES' : [500, 502, 503, 504, 400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 429]
     }
    
    def parse(self, response):

        for next_page in response.css('.state>a'):
            link = next_page.css('a::attr(href)').extract()[0]
            yield response.follow(link, self.parse_estado)
    
    def parse_estado(self, response):
        for next_page in response.css('.city>a'):
            link = next_page.css('a::attr(href)').extract()[0]
            yield response.follow(link, self.parse_municipio)
    
    def parse_municipio(self, response):

        for next_page in response.css('.school-category-item>a'):
             link = next_page.css('a::attr(href)').extract()[0]
             yield response.follow(link, self.parse_cat_school)
    
    def parse_cat_school(self, response):

        for school in response.css('.schools>a'):
            for link in school.css('a ::attr(href)'):
                yield response.follow(link.get(), self.parse_school)

    def parse_school(self, response):

        escola = ItemLoader(item=Escola(), response=response)

        escola.add_xpath('name', '//h1[@itemprop="name"]/text()')
        escola.add_xpath('address', '//div[@itemprop="address"]/descendant::*/text()')
        escola.add_xpath('latitude', '//meta[@itemprop="latitude"]/@content')
        escola.add_xpath('longitude', '//meta[@itemprop="longitude"]/@content')
        
              
        return escola.load_item()