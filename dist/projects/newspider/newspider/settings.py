MYSQL_TEST = dict(
  host='140.210.4.78',
  port=3306,
  db='test_abroadsystem',
  user='test_openzsjw',
  password='kophen#_teqsd#wtj',
  charset='utf8mb4',
)
MYSQL_TEST_TABLE = 'test_bbs_02'

IR_MEDIATYPE = 2  # 指定网站类型
IR_TRADE = -1  # 指定行业id
IR_BY3 = 92  # 客户id
IR_LIBRARIYTYPE = -1  # 地区


AREA_CODE = {
    '湘': 4000, '京': 4001, '津': 4002, '冀': 4003, '晋': 4004, '蒙': 4005, '辽': 4006, '吉': 4007,
    '黑': 4008, '沪': 4009, '苏': 4010, '浙': 4011, '皖': 4012, '闽': 4013, '赣': 4014, '鲁': 4015,
    '豫': 4016, '鄂': 4017, '粤': 4018, '桂': 4019, '琼': 4020, '渝': 4021, '川': 4022, '黔': 4023,
    '滇': 4024, '藏': 4025, '陕': 4026, '甘': 4027, '青': 4028, '宁': 4029, '新': 4030, '湖南': 4000,
    '北京': 4001, '天津': 4002, '河北': 4003, '山西': 4004, '内蒙古': 4005, '辽宁': 4006, '吉林': 4007,
    '黑龙江': 4008, '上海': 4009, '江苏': 4010, '浙江': 4011, '安徽': 4012, '福建': 4013, '江西': 4014,
    '山东': 4015, '河南': 4016, '湖北': 4017, '广东': 4018, '广西': 4019, '海南': 4020, '重庆': 4021,
    '四川': 4022, '贵州': 4023, '云南': 4024, '西藏': 4025, '陕西': 4026, '甘肃': 4027, '青海': 4028,
    '宁夏': 4029, '新疆': 4030, '香港': 1, '香港特别行政区': 1, '港': 1, '台湾': 2, '台': 2,
    '北美': 3, '欧洲': 4, '亚洲': 5, '国内': -1, '澳门': 12, '澳': 12, '美国': 1001, '英国': 1002,
    '蜀': 4022,
 }
# Redis URL，格式redis :// [: password@] host [: port] [/ database][? [timeout=timeout[d|h|m|s|ms|us|ns]] [&database=database]]
#REDIS_URL = 'redis://192.168.124.200:6379/2'
REDIS_URL = 'redis://127.0.0.1:6379/2'
# 对于任何站点，将允许爬网的最大深度。如果为零，则不施加限制
DEPTH_LIMIT = 3

# 是否收集详细的深度统计信息。如果启用此功能，则在统计信息中收集每个深度的请求数
#DEPTH_STATS_VERBOSE = False


# 包含要使用的项目管道及其顺序的字典。值是任意的，但是习惯上将它们定义在0-1000范围内。低值优先于高值
ITEM_PIPELINES = {
  'newspider.pipelines.MysqlPipeline': 300,
}

# 是否启用日志记录
#LOG_ENABLED = True

# 用于日志记录的编码
#LOG_ENCODING = 'utf-8'

# 用于记录输出的文件名
#LOG_FILE = 'n'

# 用于格式化日志消息的字符串
#LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# 用于格式化日期/时间的字符串，用于改变LOG_FORMAT 中的asctime占位符
#LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# 用于格式化不同操作的日志消息的类
#LOG_FORMATTER = "scrapy.logformatter.LogFormatter"

# 最低记录级别, 可用：CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_LEVEL = 'INFO'

# 如果为True，所有标准输出（和错误）将被重定向到日志，例如print也会被记录在日志
#LOG_STDOUT = False

# 如果为True，则日志将仅包含根路径;如果设置为False，则显示负责日志输出的组件
#LOG_SHORT_NAMES = False

# 每次统计记录打印输出之间的间隔（以秒为单位）
#LOGSTATS_INTERVAL = 60.0

# 是否启用内存调试
#MEMDEBUG_ENABLED = False

# 启用内存调试后，如果此设置不为空，则会将内存报告发送到指定的邮箱地址，否则该报告将被写入日志。
# 例如：MEMDEBUG_NOTIFY = ['user@example.com']
#MEMDEBUG_NOTIFY = []

# 是否启用内存使用扩展。此扩展跟踪该进程使用的峰值内存（将其写入统计信息）。
# 当超过内存限制时，它还可以选择关闭Scrapy进程，并在发生这种情况时通过电子邮件通知
#MEMUSAGE_ENABLED = True

# 关闭Scrapy之前允许的最大内存量
#MEMUSAGE_LIMIT_MB = 0

# 电子邮件列表，用于通知是否已达到内存限制
#MEMUSAGE_NOTIFY_MAIL = False

# 发送警告电子邮件通知最大内存之前允许的最大内存量（以兆字节为单位）。如果为零，则不会发出警告
#MEMUSAGE_WARNING_MB = 0


# 如果启用，Scrapy将在从同一网站获取请求的同时等待随机的时间（介于0.5 * DOWNLOAD_DELAY和1.5 *之间DOWNLOAD_DELAY）
#RANDOMIZE_DOWNLOAD_DELAY = True

# Twisted Reactor线程池大小的最大限制。这是各种Scrapy组件使用的通用多用途线程池。
# 线程DNS解析器，BlockingFeedStorage，S3FilesStore仅举几例。
# 如果遇到阻塞IO不足的问题，请增加此值。
#REACTOR_THREADPOOL_MAXSIZE = 10

# 定义可以重定向请求的最长时间。超过此最大值后，将按原样返回请求的响应
#REDIRECT_MAX_TIMES = 20

# 调整重定向请求的优先级，为正则优先级高
#REDIRECT_PRIORITY_ADJUST = 2

# 调整重试请求的优先级
#RETRY_PRIORITY_ADJUST = -1

# 设置为True将记录有关请求调度程序的调试信息
#SCHEDULER_DEBUG = False

# 正在处理响应数据的软限制（以字节为单位）。
# 如果所有正在处理的响应的大小总和高于此值，Scrapy不会处理新的请求
#SCRAPER_SLOT_MAX_ACTIVE_SIZE  = 5_000_000

# 包含您的项目中启用的蜘蛛中间件及其命令的字典
#SPIDER_MIDDLEWARES = {}

#SPIDER_MIDDLEWARES_BASE = {
#     'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
#     'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
#     'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
#     'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
#     'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
# }

# 用于收集统计信息的类
#STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'

# 蜘蛛完成后，将Scrapy统计信息转储到Scrapy日志中
#STATS_DUMP = True

# 蜘蛛抓取完毕后发送Scrapy统计信息的邮箱列表
#STATSMAILER_RCPTS = []

# 项目名称
BOT_NAME = 'newspider'
SPIDER_MODULES = ['newspider.spiders']
NEWSPIDER_MODULE = 'newspider.spiders'
# 是否遵循robot协议
ROBOTSTXT_OBEY = False
# 指定是否 将启用telnet控制台
TELNETCONSOLE_ENABLED = False
# 爬网时使用的默认User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
# scrapy-redis配置
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# 下载程序的超时时间（以秒为单位）
DOWNLOAD_TIMEOUT = 15
# 用于Scrapy HTTP请求的默认标头。它们被填充在 DefaultHeadersMiddleware

COMMANDS_MODULE = 'newspider.commands'
#布隆过滤器的设置
BLOOMFILTER_HASH_NUMBER = 10
BLOOMFILTER_BIT = 30
SCHEDULER_PERSIST = False
# 在项目处理器（也称为“ 项目管道”）中并行处理的最大并发项目数（每个响应），默认100。
CONCURRENT_ITEMS = 100
# Scrapy下载器将执行的并发（即，并发）请求的最大数量，默认16
CONCURRENT_REQUESTS = 64
# 从同一网站下载连续页面之前，下载程序应等待的时间（以秒为单位）。
# 这可以用来限制爬网速度，以避免对服务器造成太大的冲击。支持小数。
# 默认情况下，Scrapy不会在请求之间等待固定的时间，而是使用0.5 * DOWNLOAD_DELAY和1.5 * DOWNLOAD_DELAY之间的随机间隔。
DOWNLOAD_DELAY = 0.5
# 将对任何单个域执行的并发（即，并发）请求的最大数量，默认8
CONCURRENT_REQUESTS_PER_DOMAIN = 4
# 禁用cookies中间件
COOKIES_ENABLED = False
# 处理DNS查询的超时时间（以秒为单位）。支持浮动
DNS_TIMEOUT = 15
# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

INFLUXDB_PARAMS = {
  'host': 'www.blisst.cn',
  'port': 2048,
  'username': 'kanade',
  'password': 'blisst',
  'database': 'spider'
}
INTERVAL = 5   # 存取到influxdb的时间间隔

LOG_SHORT_NAMES = True
# 包含您的项目中启用的下载器中间件及其命令的字典
DOWNLOADER_MIDDLEWARES  = {
  #'newspider.middlewares.StatCollectorMiddleware': 601
  
}

EXTENSIONS = {
    'newspider.extensions.SpiderStatLogging': 1,
}

# Scrapy中默认启用的下载程序中间件的字典。低值更接近引擎，高值更接近下载器，
# 不要试图修改此设置，请修改DOWNLOADER_MIDDLEWARES
# DOWNLOADER_MIDDLEWARES_BASE = {
#     'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
#     'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
#     'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
#     'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
#     'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
#     'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
#     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
#     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
#     'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
# }