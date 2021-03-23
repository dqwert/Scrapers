# -*- coding: utf-8 -*-
import scrapy
from tianya.items import TianyaItem

class ThemePostSpider(scrapy.Spider):
    name = 'theme-post'
    allowed_domains = ['bbs.tianya.cn']
    start_urls = ['http://bbs.tianya.cn/list.jsp?item=828&order=1/']
    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    cookies = {}
    header = {
        'User-Agent': 'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit /537.36(KHTML, likeGecko) Chrome / 54.0.2840.71Safari / 537.36'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header, meta=self.meta)

    def parse(self, response):
        if response.status != 200:
            return
        for i in range(2, 9):
            for j in range(1, 10):
                url = response.xpath('//*[@id="main"]/div[7]/table/tbody[' + str(i) + ']/tr[' + str(j) +']/td[1]/a').extract()
                print('i = ' + i + ', j = ' + j)
                print(url)

    def get_url(self, response):
        scrapy.Selector(response).xpath('//*[@id="main"]/div[7]/table/tbody[9]/tr[10]/td[1]/a').extract()

