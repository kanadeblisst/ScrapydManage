# -*- coding: utf-8 -*-
import pymysql
import logging
import os
import json
import time
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)

class MysqlPipeline(object):
 
    def __init__(self, params, table, ir_by3, bot_name):
        self.table = table
        self.sql_params = params
        self.ir_by3 = ir_by3
        self.items = []
        self.bot_name = bot_name
        self.bot_dir = self.find_bot_dir()
        self.sql = '''INSERT INTO {} (ir_title, ir_authors, ir_urltime, ir_nresrved1, ir_nresrved2, ir_nresrved3, 
                    ir_readnum, ir_label, ir_content, ir_trade, ir_area, ir_mediatype, ir_mediasource, ir_url, ir_md5, 
                    ir_urldate, ir_keyword, ir_by4, ir_spidersource, ir_by3, ir_librariytype, ir_firstauthor, ir_istrand) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(self.table)
        
    @classmethod
    def from_crawler(cls, crawler):
        params = crawler.settings.get('MYSQL_TEST')
        if not params:
            raise NotConfigured
        table = crawler.settings.get('MYSQL_TEST_TABLE')
        ir_by3 = crawler.settings.get('IR_BY3')
        bot_name = crawler.settings.get('BOT_NAME')
        o = cls(params, table, ir_by3, bot_name)
        crawler.signals.connect(o.engine_started, signal=signals.engine_started)
        crawler.signals.connect(o.engine_stopped, signal=signals.engine_stopped)
        return o

    def engine_started(self):
        self.conn = pymysql.connect(**self.sql_params)
        self.cursor = self.conn.cursor()

    def engine_stopped(self):
        while True:
            if not self.insert_many(self.items):
                continue
            time.sleep(5)
        os.chdir(self.bot_dir + '/datas')
        while True:
            for file in os.listdir():
                with open(file, encoding='utf-8') as f:
                    items = json.loads(f.read())
                if self.insert_many(items):
                    os.remove(file)
                else:
                    break
            if os.listdir():
                time.sleep(5)
                continue
            else:
                break
        self.conn.close()

    def find_bot_dir(self):
        curdir = os.getcwd()
        if curdir.endswith('rules') or curdir.endswith('spiders'):
            return curdir.strip('/rules').strip('/spiders')
        elif curdir.endswith(self.bot_name):
            return curdir if curdir.count(self.bot_name) == 2 else curdir + '/' + self.bot_name
        else:
            logger.error('当前目录异常，请检查后重试! ')

    def process_item(self, item, spider):
        #if self.items.__sizeof__() > 1000000:
        if len(self.items) > 10:
            if self.insert_many(self.items):
                logger.info(f'成功插入{len(self.items)}条数据！')
            else:
                file = '/data/' + str(int(time.time())) + '.json'
                with open(self.bot_dir + file , 'w', encoding='utf-8') as fw:
                    fw.write(json.dumps(self.items))
                logger.info(f'插入数据失败！已保存为文件{file}')
            self.items.clear()
        else:
            logger.info(f'当前数据不足，不执行插入，数据量({len(self.items)}),数据大小：{self.items.__sizeof__()}')
        self.items.append(dict(item))
        return item

    def insert_many(self, items):
        values = [( item.get('ir_title'), item.get('ir_authors'), item.get('ir_urltime'),
                    item.get('ir_nresrved1', None), item.get('ir_nresrved2', None), item.get('ir_nresrved3', None),
                    item.get('ir_readnum', None), item.get('ir_label', None), item.get('ir_content'),
                    item.get('ir_trade', -1), item.get('ir_area', 2), item.get('ir_mediatype'),
                    item.get('ir_mediasource'), item.get('ir_url'), item.get('ir_md5'),
                    item.get('ir_urldate'), item.get('ir_keyword', None), item.get('ir_by4', None), item.get("ir_spidersource", 2),
                    item.get("ir_by3", self.ir_by3), item.get("ir_librariytype"), item.get("ir_firstauthor", None), item.get("ir_istrand", 1)) for item in items]
        try:
            self.cursor.executemany(self.sql, values)
        except Exception as err:
            logger.debug(err)
            return False
        else:
            self.conn.commit()
            return True
