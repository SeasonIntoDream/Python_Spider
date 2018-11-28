# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from scrap_selenium_taobao.items import ScrapSeleniumTaobaoItem

class TaobaoSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    base_url = 'https://search.jd.com/Search?enc=utf-8&vt=2&page={}&keyword='
    
    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = self.base_url.format(str(page)) + quote(keyword)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
    
    def parse(self, response):
        produce_list = response.xpath('//div[@id="J_goodsList"]/ul/li')
        
        for produce in produce_list:
            item = ScrapSeleniumTaobaoItem()
            
            name3 = produce.xpath('./div/div[4]/a/em/text()').extract()
            item['name'] = "".join(name3)
            
            b = produce.xpath('.//div[contains(@class,"price")]/strong/i/text()').extract_first()
            if b:
                item['price'] = b
            else:
                item['price'] = " "
            
            c = produce.xpath('./div/div[5]/strong/a/text()').extract_first()
            d = produce.xpath('./div/div[5]/strong/text()').extract_first()
            # item['comment'] = self.judge(c, d)
            item['comment'] = c + d
            item['shop'] = produce.xpath('./div/div[7]//span/a/@title').extract_first()

            yield item
