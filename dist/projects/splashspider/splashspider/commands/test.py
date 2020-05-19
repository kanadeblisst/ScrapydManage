import sys
import os
import json
import string
import logging
from importlib import import_module
from scrapy.utils.spider import iter_spider_classes
from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError


logger = logging.getLogger(__name__)

def create_spider(setting_rule, fname):
    allowed_domains = json.dumps(setting_rule.get('allowed_domains'), ensure_ascii=False)
    start_urls = json.dumps(setting_rule.get('start_urls'), ensure_ascii=False)
    article_url = json.dumps(setting_rule.get('article_url'), ensure_ascii=False)
    re_article_url = json.dumps(setting_rule.get('re_article_url'), ensure_ascii=False)
    ir_mediatype = json.dumps(setting_rule.get('ir_mediatype'), ensure_ascii=False)
    ir_mediasource = json.dumps(setting_rule.get('ir_mediasource'), ensure_ascii=False)
    ir_librariytype = json.dumps(setting_rule.get('ir_librariytype'), ensure_ascii=False)
    ir_trade = json.dumps(setting_rule.get('ir_trade', -1), ensure_ascii=False)
    ir_area = json.dumps(setting_rule.get('ir_area', 2), ensure_ascii=False)
    extract_rule = json.dumps(setting_rule.get('extract_rule'), ensure_ascii=False)
    d = { 
            'classname': 'RuleSpider', 'name': fname, 'allowed_domains': allowed_domains, 'start_urls': start_urls,
            'article_url': article_url, 're_article_url': re_article_url, 'ir_mediatype': ir_mediatype, 
            'ir_mediasource': ir_mediasource, 'ir_librariytype': ir_librariytype, 'ir_trade': ir_trade, 
            'ir_area': ir_area, 'extract_rule': extract_rule,
        }
    with open('../tempspider.py', 'r', encoding='utf-8') as f:
        tempstr = f.read()
    with open(f'../spiders/{fname}_spider.py', 'w', encoding='utf-8') as fw:
        fw.write(string.Template(tempstr).substitute(d).replace('true', 'True').replace('false', 'False').replace('null', 'None'))

def _import_file(filepath):
    abspath = os.path.abspath(filepath)
    dirname, file = os.path.split(abspath)
    logging.info(dirname) 
    fname, fext = os.path.splitext(file)
    if fext != '.py':
        raise ValueError("Not a Python source file: %s" % abspath)
    if dirname:
        sys.path = [dirname] + sys.path
    with open(filepath, encoding='utf-8') as f:
            s = f.read()
    s = s.replace('"title":', '"ir_title":')
    s = s.replace('"column":', '"ir_by4":')
    s = s.replace('"author":', '"ir_authors":')
    s = s.replace('"pub_time":', '"ir_urltime":')
    s = s.replace('"content":', '"ir_content":')
    s = s.replace('"label":', '"ir_label":')
    s = s.replace('"share_num":', '"ir_nresrved1":')
    s = s.replace('"like_num":', '"ir_nresrved2":')
    s = s.replace('"comment_num":', '"ir_nresrved3":')
    s = s.replace('"read_num":', '"ir_readnum":')
    with open(filepath, 'w', encoding='utf-8') as fw:
        fw.write(s)
    try:
        module = import_module(fname)
    except Exception as e:
        logger.error('模板文件可能有语法错误，请检查后重试！(%s)' % str(e))
    else:
        create_spider(module.setting_rule, fname)
        sys.path = [dirname+'/../spiders'] + sys.path
        spider_module = import_module(f'{fname}_spider')
        return spider_module
    finally:
        if dirname:
            sys.path.pop(0)
            sys.path.pop(0)


class Command(ScrapyCommand):

    requires_project = True
    
    def syntax(self):
        return "<spider_file>"

    def short_desc(self):
        return "Run a self-contained spider (without creating a project)"

    
    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError()
        filename = args[0]
        if not os.path.exists(filename):
            raise UsageError("File not found: %s\n" % filename)
        try:
            spider_module = _import_file(filename)
        except (ImportError, ValueError) as e:
            raise UsageError("Unable to load %r: %s\n" % (filename, e))

        spclasses = list(iter_spider_classes(spider_module))
        if not spclasses:
            raise UsageError("No spider found in file: %s\n" % filename)
        spidercls = spclasses.pop()

        self.crawler_process.crawl(spidercls, **opts.__dict__)
        self.crawler_process.start()

        if self.crawler_process.bootstrap_failed:
            self.exitcode = 1
