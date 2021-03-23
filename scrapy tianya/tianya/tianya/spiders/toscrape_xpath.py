# -*- coding: utf-8 -*-
import scrapy


class ToscrapeXpathSpider(scrapy.Spider):
    name = 'toscrape-xpath'
    allowed_domains = ['bbs.tianya.cn']
    start_urls = ['http://bbs.tianya.cn/list.jsp?item=828&order=1/']
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }
    cookies = {}
    header = {
        'User-Agent': 'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit /537.36(KHTML, likeGecko) Chrome / 54.0.2840.71Safari / 537.36'}

    def parse(self, response):
        for quote in response.xpath('//*[@id="main"]/div[7]/table/tbody[2]'):
            yield {
                'text': quote
            }

        next_page_url = response.xpath('//*[@id="main"]/div[8]/div/a[2]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

