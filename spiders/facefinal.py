# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy import Selector
from practice.items import PracticeItem
from scrapy_splash import SplashRequest
import logging
import re
class FacebookSpider(scrapy.Spider):
	name = 'facefinal'
	last_news = ""
	last_comment = ""
	allowed_domains = ['facebook.com']
	start_urls = ['https://www.facebook.com/login/']
	count = 0
	urls = ["https://www.facebook.com/bbcnews/posts/","https://www.facebook.com/ZeeNewsEnglish/posts/","https://www.facebook.com/masrur.englishnews/posts/","https://www.facebook.com/TurkeyEnglishNews/posts/","https://www.facebook.com/pg/kbsnewsenglish/posts/","https://www.facebook.com/GermanyEnglishNews/posts/","https://www.facebook.com/IranEnglishNews1/posts/","https://www.facebook.com/English-Premier-League-News-366134440144729/posts/","https://www.facebook.com/euronews/posts/","https://www.facebook.com/i24newsEN/posts/","https://www.facebook.com/RussiaEnglishNews/posts/","https://www.facebook.com/ThaiPBSEnglishNews/posts/","https://www.facebook.com/NewJapanProNewsFeed/posts/","https://www.facebook.com/BreakingNewsEnglish-155625444452176/posts/","https://www.facebook.com/cnnnews18/posts/","https://www.facebook.com/aljazeera/posts/","https://www.facebook.com/OrientNewsEn/posts/","https://www.facebook.com/msnbc/posts/","https://www.facebook.com/skynews/posts/","https://www.facebook.com/cnn/posts/","https://www.facebook.com/cnninternational/posts","https://www.facebook.com/FoxNews/posts/","https://www.facebook.com/GeoEnglishdotTV/posts/","https://www.facebook.com/ndtv/posts/","https://www.facebook.com/FRANCE24.English/posts/","https://www.facebook.com/PRESSTV/posts/","https://www.facebook.com/Timesnow/posts/","https://www.facebook.com/TimesofIndia/posts/","https://www.facebook.com/voiceofamerica/posts/","https://www.facebook.com/cctvcom/posts/","https://www.facebook.com/bloombergbusiness/posts/","https://www.facebook.com/ABCNews/posts/",]
	url = ""
	script = 'function main(splash)assert(splash:go(splash.args.url))local get_dimensions = splash:jsfunc([[function () {var rect = document.getElementsByClassName("uiMorePagerPrimary")[0].getClientRects()[0];return {"x": rect.left, "y": rect.top}}]])	splash:set_viewport_full()splash:wait(0.1)local dimensions = get_dimensions()splash:mouse_click(dimensions.x, dimensions.y)splash:wait(0.1)return splash:html()end'
	def parse(self,response):
		self.url = self.urls[self.count]
		return FormRequest.from_response(response,dont_filter=True,formdata={"email":"chakraborty.soumik23@gmail.com","pass":"asusmicromax"},callback=self.after_login)
	def after_login(self,response):
		return scrapy.Request(self.url,callback=self.search_news)
	def search_news(self,response):
		self.count = self.count+1
		logging.warning(self.count)
		return scrapy.Request(response.url,callback=self.seemore,dont_filter=True,meta={
                'splash': {
                    'args': {'lua_source': self.script,'wait': 0.5,},
                    'endpoint': 'execute',
                }
            })
	def seemore(self,response):
		item = PracticeItem()
		select = scrapy.selector.Selector(text=response.body,type="html")
		matters = select.re('js_[a-zA-Z0-9]+"><p>[^<]+<|UFICommentActorName"[^<]+<|UFICommentBody"><span>[^<]+<')
		for matter in matters:
			if(re.findall(r"js_",matter)):
				self.last_news = re.findall(">[^<]+",matter)
			if(re.findall(r"UFICommentActorName",matter)):
				self.last_commentor = re.findall(">[^<]+",matter)
			if(re.findall(r"UFICommentBody",matter)):
				item['news'] = self.last_news
				item['commentor'] = self.last_commentor
				item["comments"] = re.findall(">[^<]+",matter)
				yield item
		yield scrapy.Request("https://www.facebook.com/login/",dont_filter=True,callback=self.parse)