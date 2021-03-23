import scrapy
from tianya.items import TianyaItem

class TechcrunchSpider(scrapy.Spider):
    # name of the spider
    name = 'techcrunch'

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }
    cookies = {}
    header = {
        'User-Agent': 'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit /537.36(KHTML, likeGecko) Chrome / 54.0.2840.71Safari / 537.36'}

    # list of allowed domains
    allowed_domains = ['bbs.tianya.cn']

    # starting url for scraping
    start_urls = ['http://bbs.tianya.cn/list.jsp?item=828&order=1/']

    count = 0

    fileName = 'tianya.txt'  # 爬取的内容存入文件，文件名为：作者-语录.txt
    f = open(fileName, "a+")  # 追加写入文件

    # setting the location of the output csv file
    custom_settings = {
        'FEED_URI': 'temp/tianya.csv'
    }

    def parse(self, response):
        # print('[test] ' + str(self.count + 1) + 'th run')
        for i in range(2, 9):
            for j in range(1, 10):
                post_url = str('http://bbs.tianya.cn' + response.xpath(
                    '//*[@id="main"]/div[7]/table/tbody[' + str(i) + ']/tr[' + str(j) +']/td[1]/a/@href').extract_first())
                # print('i = ' + str(i) + ', j = ' + str(j) + '\tresult: ' + post_url)
                yield scrapy.http.Request(post_url, callback=self.process_post)

        if self.count == 0:
            next_page_url = response.xpath('//*[@id="main"]/div[8]/div/a[2]/@href').get()
        else:
            next_page_url = response.xpath('//*[@id="main"]/div[8]/div/a[3]/@href').get()
        if next_page_url is not None:
            self.count += 1
            yield scrapy.Request(response.urljoin(next_page_url))

    def process_post(self, response):
        post_content = ""
        for para in response.xpath('//*[@id="bd"]/div[4]/div[1]/div/div[2]/div[1]/text()').extract():
            post_content = post_content + para
        post_content = post_content.replace("\r", "").replace('\r\n', '').replace('\t', '').replace('\u3000', '').replace('\n', "")
        # print("------- [post content] -------\n" + str(type(post_content)) + post_content)
        item = TianyaItem()
        item['post_url'] = response.url
        item['post_title'] = response.xpath('//*[@id="post_head"]/h1/span[1]/span/text()').extract()[0]
        item['post_time'] = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[2]/text()').extract()[0][3:-1]
        item['reply_num'] = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[4]/text()').extract()[0][3:]
        item['content'] = post_content
        item['author'] = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[1]/a/text()').extract()[0]
        item['author_id'] = response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[1]/a/@href').extract()[0]
        # print(type(item['content']))
        yield item
