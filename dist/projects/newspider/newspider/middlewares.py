# -*- coding: utf-8 -*-
import time
import logging
import requests
 
logger = logging.getLogger(__name__)

class StatCollectorMiddleware(object):
    def __init__(self):
        pass

    def process_request(self, request, spider):
        stats = spider.crawler.stats.get_stats()
        logger.warning(stats)

   