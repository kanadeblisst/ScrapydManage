#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashTextResponse, SplashJsonResponse, SplashResponse
from scrapy.http import HtmlResponse

class MySpider(CrawlSpider):
    name = 'csdn'
    url = ['https://www.csdn.net/']
    allowed_domains = ["csdn.net"]
    rules = (
        Rule(LinkExtractor(allow=('.*',)), callback='parse_item', process_request='splash_request', follow=True),
    )

    def start_requests(self):
        for url in self.url:
            # Splash 默认是render.html,返回javascript呈现页面的HTML。
            yield SplashRequest(url, args={'wait': 0.5})

    # 这个方法是给Rule 中的process_request用的。
    def splash_request(self, request):
        request.meta.update(splash={
            'args': {
                'wait': 1,
            },
            'endpoint': 'render.html',
        })
        return request
    def parse_item(self,response):
        self.logger.debug(response.url)

    # 重写CrawlSpider 的方法
    def _requests_to_follow(self, response):
        seen = set()

        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)
              
    


