# -*- coding: utf-8 -*-
import scrapy


class DocuSpider(scrapy.Spider):
    name = 'docu'
    allowed_domains = ['web']
    start_urls = ['http://web/']

    def parse(self, response):
        pass
