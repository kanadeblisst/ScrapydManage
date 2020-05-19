import time
import hashlib

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from newspider.items import RuleSpiderItem
from newspider.extract_time import ExtractTime


class $classname(CrawlSpider):
    name = '$name' 
    allowed_domains = $allowed_domains
    start_urls = $start_urls
    time_extracter = ExtractTime()
    article_url = $article_url
    rules = (
        Rule(LinkExtractor(allow=article_url.keys()), callback='parse_content', follow=True),
    ) if article_url else []
    
    def parse_content(self, response):
        re_article_url = $re_article_url
        if re_article_url:
            for re_ in re_article_url:
                for url in response.re(re_):
                    yield response.follow(url, callable=self.parse_content)

        ir_mediasource = $ir_mediasource
        ir_mediatype = $ir_mediatype
        ir_librariytype = $ir_librariytype
        ir_trade = $ir_trade
        ir_area = $ir_area

        _url = response.url
        l = ItemLoader(item=RuleSpiderItem(), response=response)
        l.add_value('ir_mediasource', ir_mediasource)
        l.add_value('ir_mediatype', ir_mediatype)
        l.add_value('ir_librariytype', ir_librariytype)
        l.add_value('ir_trade', ir_trade)
        l.add_value('ir_area', ir_area) 
        l.add_value('ir_urldate', int(time.time()))
        l.add_value('ir_url', _url)
        extract_rule = $extract_rule
        for key in extract_rule:
            xpaths = extract_rule[key].get('xpath')
            if xpaths:
                for xpath in xpaths:
                    l.add_xpath(key, xpath)
            re_list = extract_rule[key].get('re')
            if re_list:
                for re_ in re_list:
                    l.add_xpath(key, '/html', re=re_)
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
        self.logger.info('时间字符串：%s, 解析出的时间：%s'% (timestr, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))))
        l.replace_value('ir_urltime', int(timestamp))
        l.add_value('ir_istrand', self.is_forward(ir_mediasource, l.get_collected_values('ir_firstauthor'))) 
        l.add_value('ir_md5', hashlib.md5(_url.encode('utf-8')).hexdigest())
        #self.logger.info(l.load_item())
        yield l.load_item()
        
            
    def is_forward(self, ir_mediasource, ir_firstauthor):
        if not ir_firstauthor:
            return 1
        return 1 if set(ir_mediasource) & set(ir_firstauthor) else 2