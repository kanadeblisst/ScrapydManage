# -*- coding: utf-8 -*-
import os
import json
import logging
import string
import sys
import redis
from importlib import import_module
from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import UsageError
from scrapy.utils.spider import iter_spider_classes


logger = logging.getLogger(__name__)

def get_bot_dir():
    curdir = os.getcwd()
    bot_name = get_project_settings().get('BOT_NAME')
    if curdir.endswith('rules') or curdir.endswith('spiders') or curdir.endswith('rules'):
        return curdir.strip('rules').strip('spiders').strip('rules').strip(os.sep)
    elif curdir.endswith(bot_name):
        return curdir if curdir.count(bot_name) == 2 else curdir + os.sep + bot_name
    else:
        if bot_name in os.listdir():
            return curdir + os.sep + bot_name
        else:
            logger.error(f'当前目录异常，请检查后重试!{curdir} ')
        

def _create_spider(setting_rule, fname, path):
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
    
    with open(path + os.sep + 'tempspider.py', 'r', encoding='utf-8') as f:
        tempstr = f.read()
    with open(path + os.sep + f'spiders/{fname}_spider.py', 'w', encoding='utf-8') as fw:
        fw.write(string.Template(tempstr).substitute(d).replace('true', 'True').replace('false', 'False').replace('null', 'None'))

def create_spider(filepath, path):
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
        _create_spider(module.setting_rule, fname, path)
    finally:
        if dirname:
            sys.path.pop(0)

def _import_file(filepath):
    abspath = os.path.abspath(filepath)
    dirname, file = os.path.split(abspath)
    fname, fext = os.path.splitext(file)
    if fext != '.py':
        raise ValueError("Not a Python source file: %s" % abspath)
    if dirname:
        sys.path = [dirname] + sys.path
    try:
        module = import_module(fname)
    finally:
        if dirname:
            sys.path.pop(0)
    return module

class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        r = redis.Redis(decode_responses=True)
        r.set('scrapyPID', str(os.getpid()))
        
        bot_dir = get_bot_dir()
        for rule in os.listdir(bot_dir + os.sep + 'rules'):
            if not rule.endswith('.py'):
                continue
            
            create_spider(bot_dir + os.sep + 'rules' + os.sep + rule, bot_dir)
        for file in os.listdir(bot_dir + os.sep + 'spiders'):
            if not file.endswith('.py'):
                continue
            try:
                module = _import_file(bot_dir + os.sep + 'spiders' + os.sep + file)
            except (ImportError, ValueError):
                logger.error(f'导入{file}模块错误')
                continue
            spclasses = list(iter_spider_classes(module))
            if not spclasses:
                continue
            spidercls = spclasses.pop()

            self.crawler_process.crawl(spidercls,**opts.__dict__)
        self.crawler_process.start()

        if self.crawler_process.bootstrap_failed:
            self.exitcode = 1