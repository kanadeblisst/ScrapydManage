import time
import re
import logging

logger = logging.getLogger(__name__)

class ExtractTime(object):
    time_pattern = [
        # 01/03/2019 01:23
        r'(?P<day>[0123]?\d)[-日号/號\s\.]+(?P<month>[01]?\d)[-/\s月\.]+(?P<year>20[012]\d)[-/\s年\.,]+(?P<hour>\d+):(?P<minute>\d+):(?P<seconds>\d+)',
        r'(?P<day>[0123]?\d)[-日号/號\s\.]+(?P<month>[01]?\d)[-/\s月\.]+(?P<year>20[012]\d)[-/\s年\.,]+(?P<hour>\d+):(?P<minute>\d+)(?P<seconds>)',
        r'(?P<day>[0123]?\d)[-日号/號\s\.]+(?P<month>[01]?\d)[-/\s月\.]+(?P<year>20[012]\d)[-/\s年\.,]+(?P<hour>\d+)(?P<minute>)(?P<seconds>)',
        r'(?P<day>[0123]?\d)[-日号/號\s\.]+(?P<month>[01]?\d)[-/\s月\.]+(?P<year>20[012]\d)(?P<hour>)(?P<minute>)(?P<seconds>)',
        # 2019年05月10日04:38:10
        r'(?P<year>20[012]\d)[-/\s年\.,]+(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日号/號\s\.]+(?P<hour>\d+):(?P<minute>\d+):(?P<seconds>\d+)', 
        r'(?P<year>20[012]\d)[-/\s年\.,]+(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日号/號\s\.]+(?P<hour>\d+):(?P<minute>\d+)(?P<seconds>)',
        r'(?P<year>20[012]\d)[-/\s年\.,]+(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日号/號\s\.]+(?P<hour>\d+)(?P<minute>)(?P<seconds>)',
        r'(?P<year>20[012]\d)[-/\s年\.,]+(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日号/號\s\.]*(?P<hour>)(?P<minute>)(?P<seconds>)',
        # 05月10日2019年 04:38:10
        r'(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日号/號\s\.,]*(?P<year>20[012]\d)[-/\s年\.]+(?P<hour>\d+):(?P<minute>\d+):(?P<seconds>\d+)',
        r'(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日号/號\s\.,]*(?P<year>20[012]\d)[-/\s年\.]+(?P<hour>\d+):(?P<minute>\d+)(?P<seconds>)',
        r'(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日号/號\s\.,]*(?P<year>20[012]\d)[-/\s年\.]+(?P<hour>\d+)(?P<minute>)(?P<seconds>)',
        r'(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日号/號\s\.,]*(?P<year>20[012]\d)[-/\s年\.]*(?P<hour>)(?P<minute>)(?P<seconds>)',
        # 19年05月10日04:38:10
        r'(?P<year>[012]\d)[-/\s年\.]+(?P<month>[01]?\d)[-/\s月\.]*(?P<day>[0123]?\d)[-日/号號\s\.]+(?P<hour>\d+):(?P<minute>\d+):(?P<seconds>\d+)',
        r'(?P<year>[012]\d)[-/\s年\.]+(?P<month>[01]?\d)[-/\s月\.]*(?P<day>[0123]?\d)[-日/号號\s\.]+(?P<hour>\d+):(?P<minute>\d+)(?P<seconds>)',
        r'(?P<year>[012]\d)[-/\s年\.]+(?P<month>[01]?\d)[-/\s月\.]*(?P<day>[0123]?\d)[-日/号號\s\.]+(?P<hour>\d+)(?P<minute>)(?P<seconds>)',
        r'(?P<year>[012]\d)[-/\s年\.]+(?P<month>[01]?\d)[-/\s月\.]*(?P<day>[0123]?\d)[-日/号號\s\.]*(?P<hour>)(?P<minute>)(?P<seconds>)',
        # 05月10日04:38:10
        r'(?P<year>)(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日/号號\s\.]+(?P<hour>\d+):(?P<minute>\d+):(?P<seconds>\d+)',
        r'(?P<year>)(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日/号號\s\.]+(?P<hour>\d+):(?P<minute>\d+)(?P<seconds>)',
        r'(?P<year>)(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日/号號\s\.]+(?P<hour>\d+)(?P<minute>)(?P<seconds>)',
        r'(?P<year>)(?P<month>[01]?\d)[-/\s月\.]+(?P<day>[0123]?\d)[-日/号號\s\.]*(?P<hour>)(?P<minute>)(?P<seconds>)',
        # 15:30
        r'(?P<year>)(?P<month>)(?P<day>)(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<seconds>\d{1,2})',
        r'(?P<year>)(?P<month>)(?P<day>)(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):?(?P<seconds>)',
    ]
    time_word = {
        r'()今\s*天': int(time.time()),
        r'()昨\s*天': int(time.time()) - 86400,
        r'()前\s*天': int(time.time()) - 86400*2,
        r'(\d+)\s*天\s*前':  lambda x:(int(time.time()) - 86400*x) ,#一二三四五六七八九十
        r'(\d+)\s*[周週]\s*前':  lambda x:(int(time.time()) - 7 * 86400*x),
        r'(\d+)\s*年\s*前':  lambda x:(int(time.time()) - 365 * 86400*x),
        r'(\d+)\s*个?\s*月\s*前':  lambda x:(int(time.time()) - 30 * 86400*x),
        r'(\d+)小\s*[时時]\s*前': lambda x:(int(time.time()) - 3600*x),
        r'()半\s*小\s*[时時]\s*前': int(time.time()) - 1800,
        r'(\d+)\s*分\s*[钟鐘]\s*前': lambda x:(int(time.time()) - 60*x),
        r'(\d+)\s*秒\s*前': int(time.time()),
    }
    english_time = {
        'month_word' :[# AUGUST 15th, 2019 AT 7:47 PM
            r'(?P<month>%s)\s*(?P<day>[0123]*\d)[\.,snrt][tdh, ]*(?P<year>20[012]\d) at (?P<hour>[0-6]*\d):(?P<minute>[0-6]*\d)(?P<seconds>)\s*(?P<apm>[pa]m)?',
            r'(?P<month>%s)[\. ,-][ ,]*(?P<day>[0123]*\d)[\. ,-snrt][tdh,]*\s*(?P<year>20[012]\d)(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)',
            r'(?P<day>[0123]*\d)[\. ,-snrt][tdh,]*[ ,]*(?P<month>%s)\s*[-\., ][ ]*(?P<year>20[012]\d)(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)',
            r'(?P<year>20[012]\d)[\. ,-][ ,]*(?P<month>%s)\s*[-\., ][ ]*(?P<day>[0123]*\d)(?P<hour>)(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)'
        ],
        'abridge_month_word':[
            r'(?P<month>%s)\s*t?[snrt]*[tdh,]*\s*(?P<day>[0123]*\d)[\.,] (?P<year>20[012]\d)\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2})(?P<seconds>)\s*(?P<apm>[pa]m)',
            r'(?P<month>%s)\s*t?[\.\s,-][\s.,]*(?P<day>[0123]*\d)[-\., snrt][tdh,]*[\.\s]*(?P<year>20[012]\d)(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)',
            r'(?P<day>[0123]*\d)[\.\s,-snrt][tdh,]*[\.\s,]*(?P<month>%s)t?[-\s\.,]\s*(?P<year>20[012]\d)(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)',
            r'(?P<year>20[012]\d)[\.\s,-][\s,]*(?P<month>%s)t?[-\s\.,]\s*(?P<day>[0123]*\d)(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)',
            r'(?P<year>)(?P<day>[0123]*\d)[\s\.-]+(?P<month>%s)\s*t?(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)'
        ],
        'chinese_month':[
            r'(?P<month>%s)\s*月[\.\s,-]\s*(?P<day>[0123]*\d)[\.\s,-]\s*(?P<year>20[012]\d)(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)',
            r'(?P<day>[0123]*\d)[-\s\.](?P<month>%s)月[-\s\.,]\s*(?P<year>20[012]\d)(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)',
            r'(?P<year>20[012]\d)[年,]*\s*(?P<month>%s)月[\.,]*\s*(?P<day>[0123]*\d)[日]*(?P<hour>)(?P<minute>)(?P<seconds>)(?P<apm>)',
        ]
    }
    english_time_word = {
        r'(\d+)\s*days?\s*ago': lambda x:(int(time.time()) - 86400*int(x)),
        r'()today': int(time.time()) - 86400,
        r'()yesterday': int(time.time()) - 86400*2,
        r'(\d+)\s*hrs?\s*ago': lambda x:(int(time.time()) - 3600*int(x)),
        r'(\d+)\s*mins?\s*ago': lambda x:(int(time.time()) - 60*int(x)),
        r'(\d+)\s*minutes?\s*ago': lambda x:(int(time.time()) - 60*int(x)),
    }
    abridge_month_word = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    month_word = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october","november", "december"]
    chinese_month = [ '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二',]
        
    def __init__(self):
        pass

    def format_time(self, timestr, format='day_month_year'):
        timestr = timestr.lower()
        t = self.parse_english_time(timestr)
        if t:
            return t
        curtime = time.localtime()
        for re_ in self.time_pattern:
            t = re.search(re_, timestr)
            if not t:
                continue
            year = t.group('year') if t.group('year') else '2020'
            year = '20' + year if len(year) == 2 else year
            month = t.group('month') if t.group('month') else curtime.tm_mon
            day = t.group('day') if t.group('day') else curtime.tm_mday
            hour = t.group('hour') if t.group('hour') else '0'
            minute = t.group('minute') if t.group('minute') else '0'
            seconds = t.group('seconds') if t.group('seconds') else '0'
            #return f'{year}-{month}-{day} {hour}:{minute}:{seconds}'
            return time.mktime(time.strptime(f'{year}-{month}-{day} {hour}:{minute}:{seconds}', '%Y-%m-%d %H:%M:%S'))
    
        for word in self.time_word:
            t = re.search(word, timestr)
            if not t:
                continue
            number = int(t.group(1))
            return self.time_word[word](number) if number else self.time_word[word]
        
    def parse_english_time(self, timestr):
        t = self.match_month(timestr, self.abridge_month_word, 'abridge_month_word')
        if t:
            return t
        t = self.match_month(timestr, self.month_word, 'month_word')
        if t:
            return t
        t = self.match_month(timestr, self.chinese_month, 'chinese_month')
        if t:
            return t
        for word in self.english_time_word:
            t = re.search(word, timestr)
            if not t:
                continue
            number = int(t.group(1))
            return self.english_time_word[word](number) if number else self.english_time_word[word]
        
    def match_month(self, timestr, month_word, _str):
        if _str == 'chinese_month':
            words = month_word[::-1]
        else:
            words = month_word
        for word in words:
            if word in timestr:
                for re_ in self.english_time[_str]:
                    t = re.search(re_%word, timestr)
                    if not t:
                        continue
                    year = t.group('year') if t.group('year') else '2020'
                    year = '20' + year if len(year) == 2 else year
                    month = month_word.index(t.group('month')) + 1
                    day = t.group('day')
                    hour = t.group('hour') if t.group('hour') else '0'
                    minute = t.group('minute') if t.group('minute') else '0' 
                    seconds = t.group('seconds') if t.group('seconds') else '0'
                    apm = t.group('apm') if t.group('apm') else ''
                    if apm =='pm':
                        #return f'{year}-{month}-{day} {int(hour)+12}:{minute}:{seconds}'
                        return time.mktime(time.strptime(f'{year}-{month}-{day} {int(hour)+12}:{minute}:{seconds}', '%Y-%m-%d %H:%M:%S'))
                    else:
                        #return f'{year}-{month}-{day} {hour}:{minute}:{seconds}'
                        return time.mktime(time.strptime(f'{year}-{month}-{day} {hour}:{minute}:{seconds}', '%Y-%m-%d %H:%M:%S')) 
                    
        return False


if __name__ == "__main__":
    t = ExtractTime()
    timestr = '12:26:28'
    print('时间字符串：', timestr)
    print('解析结果:', t.format_time(timestr))