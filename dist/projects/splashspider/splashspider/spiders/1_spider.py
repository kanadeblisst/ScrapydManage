import time
import hashlib

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from splashspider.items import RuleSpiderItem
from splashspider.extract_time import ExtractTime
from scrapy_splash import SplashRequest, SplashTextResponse


class RuleSpider(CrawlSpider):
    name = '1' 
    allowed_domains = ["so.eastmoney.com", "guba.eastmoney.com", 'gb.eastmoney.com']
    time_extracter = ExtractTime()
    #article_url = {"/list": {"follow": True}, "/news": {"follow": False}, "com/a": {"follow": True}}
    def start_requests(self):
        start_urls = ["http://so.eastmoney.com/TieZi/s?keyword=中国国防金融研究会&swtype=1&pageindex=1", "http://so.eastmoney.com/CArticle/s?keyword=中国国防金融研究会&pageindex=1"]
        for url in start_urls:
            yield SplashRequest(url, args={'wait': 0.5,}, endpoint='render.html')

    rules = (
        Rule(LinkExtractor(allow=['/list', '/new']), callback='parse_content',process_request='splash_request', follow=True),
    ) 
    
   
    def parse_content(self, response):
        self.logger.debug('--------------------------------------------------------------------------------')
        # re_article_url = None
        # if re_article_url:
        #     for re_ in re_article_url:
        #         for url in response.re(re_):
        #             yield response.follow(url, callable=self.parse_content)

        ir_mediasource = "东方财富网股吧"
        ir_mediatype = 2
        ir_librariytype = "沪"
        ir_trade = 10
        ir_area = 2

        _url = response.url
        l = ItemLoader(item=RuleSpiderItem(), response=response)
        l.add_value('ir_mediasource', ir_mediasource)
        l.add_value('ir_mediatype', ir_mediatype)
        l.add_value('ir_librariytype', ir_librariytype)
        l.add_value('ir_trade', ir_trade)
        l.add_value('ir_area', ir_area) 
        l.add_value('ir_urldate', int(time.time()))
        l.add_value('ir_url', _url)
        extract_rule = {"ir_title": {"xpath": ["//div[@id=\"zwconttbt\"]/text()", "//h1[@class=\"article-title\"]//text()", "//h1/text()", "//title//text()"], "replace": ["_东方财富网股吧"]}, "ir_authors": {"xpath": ["//div[@id=\"zwconttbn\"]/strong[1]/a//text()", "//div[@id=\"zwconttbn\"]/strong//text()", "//div[@class=\"source data-source\"]/@data-source", "//div[@class=\"article-meta\"]/a/text()"], "re_findall": ["post_article[\\S\\s].*?user_nickname\":\"([\\s\\S]*?)\"", "data-json[\\S\\s].*?user_nickname\":\"([\\s\\S]*?)\""]}, "ir_urltime": {"xpath": ["//div[@class=\"zwfbtime\"]/text()", "//div[@class=\"time\"]/text()", "//div[@class=\"article-meta\"]//span//text()", "//div[@class=\"article-meta\"]//text()"]}, "ir_content": {"xpath": ["//div[@id=\"zw_body\"]", "//div[@id=\"zwconbody\"]", "//div[@id=\"ContentBody\"]", "//div[@class=\"content\"]", "//div[@class=\"article-body\"]"]}, "ir_by4": {"xpath": ["//div[@id=\"Column_Navigation\"]/a/text()", "//div[@class=\"read_path\"]/a/text()"]}, "ir_label": {}, "ir_nresrved1": {}, "ir_nresrved2": {}, "ir_nresrved3": {}, "ir_readnum": {}}
        for key in extract_rule:
            xpaths = extract_rule[key].get('xpath')
            if not xpaths:
                continue
            for xpath in xpaths:
                l.add_xpath(key, xpath)
            replaces = extract_rule[key].get('replace')
            if not replaces:
                continue
            for i in replaces:
                new_value = l.get_collected_values(key)
                if isinstance(new_value, list):
                    for value in new_value:
                        if value:
                            l.replace_value(key, value.replace(i, ''))
                if isinstance(new_value, str):
                    l.replace_value(key, new_value.replace(i, ''))
                    
        if not l.get_collected_values('ir_content'):
            self.logger.warning(f'未提取到内容，请检查后重试! 当前URL：{_url}')
            return
        t = l.get_collected_values('ir_urltime')
        if not t:
            self.logger.warning(f'未提取到时间，请检查后重试! 当前URL：{_url}')
            return
        if not l.get_collected_values('ir_title'):
            ir_content = l.get_collected_values('ir_content')
            ir_title = ir_content[:60] if len(ir_content) > 60 else ir_content
            l.add_value('ir_title', ir_title)
        for i in t:
            timestamp = self.time_extracter.format_time(i)
            if timestamp:
                timestr = i
                break
        if not timestamp:
            self.logger.warning(f'时间解析失败!，时间字符串{t}')
            return
        self.logger.debug('时间字符串：%s, 解析出的时间：%s'% (timestr, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))))
        l.replace_value('ir_urltime', int(timestamp))
        l.add_value('ir_istrand', self.is_forward(ir_mediasource, l.get_collected_values('ir_firstauthor'))) 
        l.add_value('ir_md5', hashlib.md5(_url.encode('utf-8')).hexdigest())
        self.logger.debug(l.load_item())
        yield l.load_item()
        
    def splash_request(self, request):
        request.meta.update(splash={
            'args': {
                'wait': 1,
            },
            'endpoint': 'render.html',
        })
        return request
 
    def _requests_to_follow(self, response):
        if not isinstance(response, SplashTextResponse):
            return
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

    def is_forward(self, ir_mediasource, ir_firstauthor):
        if not ir_firstauthor:
            return 1
        return 1 if set(ir_mediasource) & set(ir_firstauthor) else 2
