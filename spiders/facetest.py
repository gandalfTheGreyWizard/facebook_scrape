import scrapy
from scrapy.http import FormRequest
from scrapy import Selector
from practice.items import PracticeItem
from scrapy_splash import SplashRequest
import logging
import re
class FacebookSpider(scrapy.Spider):
	name = 'facetest'
	allowed_domains = ['facebook.com']
	start_urls = ['https://www.facebook.com/login/']
	count = 0
	last_news = ""
	last_commentor = ""
	urls = ["https://www.facebook.com/thewire.in/posts/","https://www.facebook.com/RealMadrid/posts/","https://www.facebook.com/fcbarcelona/posts/","https://www.facebook.com/Juventus/posts/","https://www.facebook.com/ChelseaFC/","https://www.facebook.com/PSG/posts/","https://www.facebook.com/BVB/posts/","https://www.facebook.com/mancity/posts/","https://www.facebook.com/manchesterunited/posts/","https://www.facebook.com/pg/GoogleIndia/posts/","https://www.facebook.com/pg/ISRO/posts/","https://www.facebook.com/NASA/posts/","https://www.facebook.com/HollywoodReporter/posts/","https://www.facebook.com/hollywoodnews/posts/","https://www.facebook.com/BollywoodNewsNetwork/posts/","https://www.facebook.com/bollywoodnewsdailyofficial/posts/","https://www.facebook.com/icc/posts/","https://www.facebook.com/olympics/posts/","https://www.facebook.com/nbcolympics/posts/","https://www.facebook.com/NBCNews/posts","https://www.facebook.com/ESPN/posts/","https://www.facebook.com/natgeo/posts/","https://www.facebook.com/AnimalPlanet/posts/","https://www.facebook.com/Discovery/posts/","https://www.facebook.com/HISTORY-238044912896496/posts/","https://www.facebook.com/nytimes/posts/","https://www.facebook.com/theguardian/posts/","https://www.facebook.com/usatoday/posts/","https://www.facebook.com/latimes/posts/","https://www.facebook.com/pg/DhruvRatheePage/posts/","https://www.facebook.com/RobertFiskonTheIndependent/posts/","https://www.facebook.com/AC360/posts/","https://www.facebook.com/AdamSchefter/posts/","https://www.facebook.com/therachelmaddowshow/posts/","https://www.facebook.com/LarryKing/posts/","https://www.facebook.com/hardwick/posts/","https://www.facebook.com/ErinAndrewsOfficial/posts/","https://www.facebook.com/ThisWeekABC/posts/","https://www.facebook.com/SanjayGuptaMD/posts/","https://www.facebook.com/rajdeepsardesai/posts/","https://www.facebook.com/BarkhaDutt/posts/","https://www.facebook.com/BJP4India/posts/","https://www.facebook.com/IndianNationalCongress/posts/","https://www.facebook.com/cpimcc/posts/","https://www.facebook.com/cpusa/posts/","https://www.facebook.com/chinadaily/posts/","https://www.facebook.com/JapanToday/posts/","https://www.facebook.com/BBCnewsAfrica/posts/","https://www.facebook.com/syrianewsofficial/posts/","https://www.facebook.com/DailyNewsEgypt/posts/","https://www.facebook.com/newsofcanada/posts/","https://www.facebook.com/7NewsAustralia/posts/","https://www.facebook.com/TheLocalSweden/posts/",]
	url = ""
	script = """
	function main(splash)
	assert(splash:go(splash.args.url))
	for i = 1,50,1 do
	local get_dimensions = splash:jsfunc([[
	function(){
		var element = document.getElementsByClassName("uiMorePagerPrimary")[0];
		if(element){
				rect = element.getBoundingClientRect()
				return {"x": rect.left+5, "y": rect.top+5}
				}
		else{ 
		return {"x":-10,"y":-10}
		}
	}
	]])
	splash:set_viewport_full()
	splash:wait(0.1)
	local dimensions = get_dimensions()
	splash:mouse_click(dimensions.x, dimensions.y)
	splash:wait(0.1)
	end
	return splash:html()
	end"""
	def parse(self,response):
		self.url = self.urls[self.count]
		return SplashRequest(self.url,callback=self.seemore,args = {'lua_source': self.script,'wait': 0.5,},endpoint='execute?timeout=3600',)	
	def seemore(self,response):
		self.count = self.count+1
		logging.warning(self.count)
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


