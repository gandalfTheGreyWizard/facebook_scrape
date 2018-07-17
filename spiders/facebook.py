# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy import Selector
from practice.items import PracticeItem
from scrapy_splash import SplashRequest
class FacebookSpider(scrapy.Spider):
	name = 'facebook'
	allowed_domains = ['facebook.com']
	start_urls = ['https://www.facebook.com/login/']

	def parse(self, response):
		return FormRequest.from_response(response,formdata={"email":"chakraborty.soumik23@gmail.com","pass":"asusmicromax"},callback=self.after_login)
	def after_login(self,response):
		urls = ["https://www.facebook.com/bbcnews/posts/",]
		for url in urls:
			yield SplashRequest(url,self.search_news,args={'wait': 0.5})
	def search_news(self,response):
		scrapy.shell.inspect_response(response,self)
		item = PracticeItem()
		body = Selector(text = response.body, type="html")
		response.selector.remove_namespaces()
		news = body.re('125;"><p>[^<]+')
		comments = body.re('body:{text:"[^"]+')
		item["news"] = news
		item["comments"] = comments
		return item
