import scrapy
from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):
    name = 'splash'
    start_urls = ["http://www.theskillinstitute.com", "http://www.indiy.in"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
                args={'wait': 0.5},
            )

    def parse(self, response):
        yield {"title":response.body}
        scrapy.shell.inspect_response(response,self)