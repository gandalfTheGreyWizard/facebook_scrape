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
	script = """
	function main(splash, args)
  	splash:go("https://www.facebook.com/bbcnews/posts/")
  	get_dim = splash:jsfunc([[
    function()
    {
    var elem = document.getElementsByClassName("UFIPagerLink");
    var arr = []
    for(var i=0;i<elem.length;i++)
    {
    	arr.push({"x":elem[i].getBoundingClientRect().left,"y":elem[i].getBoundingClientRect().top});
  	}
    return arr;
    }
    ]])
  	local dimensions = get_dim()
  	local j = 1
  	while dimensions[j] do
  		splash:set_viewport_full()
		splash:wait(0.1)
    	splash:mouse_click(dimensions[j].x, dimensions[j].y)
    	splash:wait(0.5)
    	j = j+1
  	end
  	return splash:html()
	end
	"""

	def parse(self,response):
		urls = ["https://www.facebook.com/bbcnews/posts/",]
		for url in urls:
			yield SplashRequest(url,self.search_news,args = {'lua_source': self.script,'wait': 0.5,},endpoint='execute?timeout=3600',)
	def search_news(self,response):
		resp = open("resp.html","w")
		resp.write(str(response.body))
		
