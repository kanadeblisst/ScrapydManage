import logging
from scrapy import signals
import datetime
from threading import Timer
from influxdb import InfluxDBClient


logger = logging.getLogger(__name__)

class SpiderStatLogging:

    def __init__(self, crawler, dbparams, interval):
        self.exit_code = False
        self.interval = interval
        self.crawler = crawler
        self.client = InfluxDBClient(**dbparams)
        self.stats_keys = set()
        self.cur_d = {
            'log_info': 0, 
            'log_warning': 0,
            'requested': 0,
            'request_bytes': 0,
            'response': 0,
            'response_bytes': 0,
            'response_200': 0,
            'response_301': 0,
            'response_404': 0,
            'responsed': 0,
            'item': 0,
            'filtered': 0,
        }

    @classmethod
    def from_crawler(cls, crawler):
        dbparams = crawler.settings.get('INFLUXDB_PARAMS')
        interval = crawler.settings.get('INTERVAL', 60)
        ext = cls(crawler, dbparams, interval)
        crawler.signals.connect(ext.engine_started, signal=signals.engine_started)
        crawler.signals.connect(ext.engine_stopped, signal=signals.engine_stopped)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        return ext

    def spider_closed(self, spider, reason):
        logger.info(self.stats_keys)
        influxdb_d = {
            "measurement": "spider_closed",
            "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "tags": {
                'spider_name': spider.name
            },
            "fields": {
                        'end_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                        'reason': reason,
                        'spider_name':spider.name
                    }
        }
        if not self.client.write_points([influxdb_d]):
            raise Exception('写入influxdb失败！')
        
    def spider_opened(self, spider):
        influxdb_d = {
            "measurement": "spider_opened",
            "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "tags": {
                'spider_name': spider.name
            },
            "fields": {
                        'start_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'spider_name':spider.name
                    }
        }
        if not self.client.write_points([influxdb_d]):
            raise Exception('写入influxdb失败！')

    def engine_started(self):
        Timer(self.interval, self.handle_stat).start()
    
    def engine_stopped(self):
        self.exit_code = True

    def handle_stat(self):
        stats = self.crawler.stats.get_stats()
        d = {
            'log_info': stats.get('log_count/INFO', 0), 
            'dequeued': stats.get('scheduler/dequeued/redis', 0),
            'log_warning': stats.get('log_count/WARNING', 0),
            'requested': stats.get('downloader/request_count', 0),
            'request_bytes': stats.get('downloader/request_bytes', 0),
            'response': stats.get('downloader/response_count', 0),
            'response_bytes': stats.get('downloader/response_bytes', 0),
            'response_200': stats.get('downloader/response_status_count/200', 0),
            'response_301': stats.get('downloader/response_status_count/301', 0),
            'response_404': stats.get('downloader/response_status_count/404', 0),
            'responsed': stats.get('response_received_count', 0),
            'item': stats.get('item_scraped_count', 0),
            'depth': stats.get('request_depth_max', 0),
            'filtered': stats.get('bloomfilter/filtered', 0),
            'enqueued': stats.get('scheduler/enqueued/redis', 0),
            'spider_name': self.crawler.spider.name
        }
        for key in self.cur_d:
            d[key], self.cur_d[key] = d[key] - self.cur_d[key], d[key]
        influxdb_d = {
            "measurement": "newspider",
            "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "tags": {
                'spider_name': self.crawler.spider.name
            },
            "fields": d
        }
        if not self.client.write_points([influxdb_d]):
            raise Exception('写入influxdb失败！')
        self.stats_keys.update(stats.keys())
        if not self.exit_code:
            Timer(self.interval, self.handle_stat).start()