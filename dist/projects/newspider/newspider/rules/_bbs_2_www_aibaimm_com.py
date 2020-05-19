# -*- coding: utf-8 -*-
'''
这是 通用匹配 模版
网站名称：爱败妈妈
网站主页： www.aibaimm.com
负责人： 杨可心
'''

setting_rule = {
    # 开始url 起始页
    "start_urls": ['http://www.aibaimm.com'],

    # 允许的域名
    "allowed_domains": ["www.aibaimm.com"],

    # 抓取深度 默认为10层   0 所有层 1 表示1层 2 表示2层 。。。
    # 'DEPTH_LIMIT': 10,

    # 过期时间  单位天  当天=0 昨天=1， 前天=2  1年=365
    # 'expiration_day': 1000,

    # 搜索功能
    # "search_key": {
    #     "request_url": "https://www.douban.com/search?",
    #     "form_date": {"q": "关键字", "cat": "1015"},
    #
    #     # "search_key_encode": "gb2312",
    #     "get_type": 'get',
    #     "headers": {
    #         "Host": "www.douban.com",
    #         "Referer": "https://www.douban.com/group/explore",
    #     }
    #
    # },

    # 文章url 和 下一页 可以用junk文件下url匹配检测是否合格
    # follow 表示 当前页面符合匹配链接是否继续抓取 True 表示继续 False 停止
    "article_url": {
        '.*forum-\d+-\d+\.html.*': {"follow": True},
        '.*thread-\d+-\d+-\d+\.html.*': {"follow": True},
        # '.*?link2/.*?query.*?cat_id.*': {'follow': True}
        # '.*forum.php\?mod=viewthread&tid=.*': {"follow": True},
        # '.*?\?q=.*?&sa=.*': {"follow": True},
        # '.*?/next_page-.*?\.shtml': {"follow ": True},

    },

    # 数据库固定字段 参考数据字典
    "ir_mediasource": "爱败妈妈",  # 文章媒体来源
    "ir_mediatype": 2,  # 文章媒体类型

    # 行业ID
    # 默认:-1, 政府：1, IT：2, 汽车：3, 地产：4, 时尚：5,
    # 医疗：6, 能源：7, 广告：8, 餐饮：9, 金融：10, 家居：11,
    # 通信：12, 教育：13, 航空：14, 农业：15, 旅游：16,
    # 公共安全：17, 公共交通：18, 国内医药：19, 国外医药：20
    "ir_trade": 13,  # 行业id
    "ir_area": 2,  # 监控区域  国外：1， 
    "ir_librariytype": "京",

    # 文章内容编码方式, 防止乱码
    # 'encode': 'utf-8',

    # 提取规则
    # xpath 提取规则
    # replace 替换的内容
    # handle 自定义处理函数 函数第一个参数必须为 xpath提取的内容，而且是提取的原格式list类型
    # args 自定义函数的传参 自定义函数通过关键字参数
    "extract_rule": {

        # 标题
        "ir_title": {
            'xpath': ['//h1/span[@id="thread_subject"]/text()', ]
        },

        # 作者
        "ir_authors": {
            'xpath': ['//div[@id="postlist"]/div[1]//a[@class="xw1"]/text()'],
            # 'replace': ['来自: ']
        },

        # 发布时间
        "ir_urltime": {
            'xpath': ['//div[@id="postlist"]/div[1]//div[@class="authi"]/em/span/text()','//div[@id="postlist"]/div[1]//div[@class="authi"]/em/text()'],
        },

        # 内容
        "ir_content": {
            'xpath': ['//div[@id="postlist"]/div[1]//td[@class="t_f"]//text()'],
            # "replace": [' __dzh__detail__renderGg__12();']
        },

        # 栏目
        "ir_by4": {
            'xpath': ['//*[@id="pt"]/div/a/text()']

        },

        # 标签
        "ir_label": {
            # 'xpath': ['//div[@class="mod-tags"]//text()']
        },

        # 分享数
        "ir_nresrved1": {
        },

        # 喜欢数
        "ir_nresrved2": {
            # 'xpath': ['//div[@class="posted-box-add"]//a[@title="赞"]//span[@class="c-alarm"]/text()'],
        },

        # 评论数
        "ir_nresrved3": {
            # 'xpath': ['//div[@class="forward-wblog"]/span/text()'],
        },

        # 阅读数
        "ir_readnum": {
            # 'xpath': ['//div[@class="posts-stat-c"]/div[1]/span/text()'],
        },

    },

    # 请求头, 根据网站自定义请求头
    "headers": {
        # "Host": 'search.kdnet.net'
    },
}

if __name__ == '__main__':
    pass
