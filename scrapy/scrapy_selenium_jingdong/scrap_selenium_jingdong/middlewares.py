# -*- coding: utf-8 -*-
from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger

class SeleniumMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self, timeout=5):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.chrome_options = webdriver.ChromeOptions()
        self.prefs = {'profile.default_content_setting_values.images':2}
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        # self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()
        
    def process_request(self, request, spider):
        self.logger.debug('ChromeJS is Starting...')
        # page = request.meta.get("page", 1)
        try:
            self.browser.get(request.url)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            HtmlResponse(url=request.url, status=500, request=request)
        
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
        
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
