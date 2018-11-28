import scrapy


class ScrapSeleniumTaobaoItem(scrapy.Item):
    
    name = scrapy.Field()
    price= scrapy.Field()
    commit = scrapy.Field()
    shop = scrapy.Field()
    
