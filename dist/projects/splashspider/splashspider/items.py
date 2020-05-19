# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.utils.project import get_project_settings


def area_dict(value):
    area_code = get_project_settings().get('AREA_CODE')
    return area_code.get(value, -1)

def handle_by4(value):
    return '>'.join(set(value))


class RuleSpiderItem(scrapy.Item):
    ir_title = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_authors = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_urltime = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_nresrved1 = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_nresrved2 = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_nresrved3 = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_readnum = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_label = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_content = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_trade = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_area = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_mediatype = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_mediasource = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_url = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_md5 = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_urldate = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_keyword = scrapy.Field(
        output_processor=TakeFirst(),
    )
    ir_by4 = scrapy.Field(
        input_processor=Join('>'),
        output_processor=TakeFirst(),
    )
    ir_spidersource = scrapy.Field(
        output_processor=TakeFirst(),
    )   # 保存指定列抓取
    ir_by3 = scrapy.Field(
        output_processor=TakeFirst(),
    )  # 客户id
    ir_librariytype = scrapy.Field(
        input_processor=MapCompose(area_dict),
        output_processor=TakeFirst(),
    )  # 地区
    ir_firstauthor = scrapy.Field(
        output_processor=TakeFirst(),
    )  # 来源
    ir_istrand = scrapy.Field(
        output_processor=TakeFirst(),
    )  # 是否转发