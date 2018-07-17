# -*- coding: utf-8 -*-
import scrapy
from practice.items import PracticeItem
from urllib.parse import urljoin

class BasicSpider(scrapy.Spider):
    name = 'basic'
    start_urls = [
    'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
    	for i in response.xpath('//@href').extract():
    		i = response.urljoin(i)
    		yield scrapy.Request(i,callback=self.parse)
    	yield{"title":response.xpath('//p/text()').extract()}
