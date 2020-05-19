# -*- coding: utf-8 -*-
import scrapy
import chardet
from scrapy_splash import SplashRequest

script = '''
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return {
    url = splash:url(),
    cookies = splash:get_cookies(),
    html = splash:html(),
  }
  
end
'''
class MySpider(scrapy.Spider):
    name = 'baidu'
    start_urls = ["https://www.baidu.com/"]
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.html', args={'wait':0.5})

    def parse(self, response):
        with open('a.html', 'wb') as f:
            f.write(response.body)
        self.logger.debug(response.body)