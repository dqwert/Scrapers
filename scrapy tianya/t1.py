# 账号列表
# 对应关系二维列表

from pyquery import PyQuery as pq
import requests
from urllib.parse import quote
from time import sleep

id_list_file = r'.\data\id_list.txt'
relation_file = r'.\data\re_list.txt'
page = 75
key_word = '粮食'


def prase_all_page(urls):
    """
    解析所有搜索页，获取帖子url，过滤无评论帖子
    :param urls:
    :return: content_urls
    """

    content_urls = []
    for url in urls:
        sleep(1)
        print('正在抓取：', url)
        doc = pq(requests.get(url=url, timeout=30).text)
        # print(doc)
        doc('.searchListOne li:last-child').remove()  # 删除最后一个无用li节点
        lis = doc('.searchListOne li').items()  # 获取content节点生成器
        for li in lis:
            reverse = li('.source span:last-child').text()
            print('评论数：', reverse)
            if int(reverse) <= 0:
                continue

            a = li('a:first-child')
            content_url = a.attr('href')
            content_urls.append(content_url)

    return content_urls


def prase_all_content(urls):
    """
    评论对应关系
    :param urls:
    :return:
    """

    ids = []  # id列表
    relations = []  # 关系二元组
    for url in urls:
        print('正在解析：', url)
        # sleep(1)
        doc = pq(requests.get(url=url, timeout=30).text)
        # main_id = doc('.atl-info span:first-child').attr('uid')
        main_id = doc('.atl-head .atl-menu').attr('_host')
        print('楼主id：', main_id)
        # main_name = doc('.atl-info span:first-child').attr('uname')
        # title = doc('')
        if main_id and main_id not in ids:
            ids.append(main_id)

        comments = doc('.atl-main div:gt(1)').items()  # 通栏广告后的评论列表
        for comment in comments:  # 处理评论
            host_id = comment.attr('_hostid')
            # user_name = comment.attr('_host')
            comment_text = comment('.bbs-content').text()
            replys = comment('.item-reply-view li').items()  # 评论回复
            if host_id and (host_id not in ids):
                print('评论id:', host_id)
                print('评论内容：', comment_text)
                ids.append(host_id)
                if (host_id != main_id):
                    relations.append((main_id, host_id))  # 添加楼主和评论的关系
                    print('评论关系:', main_id, '\t', host_id)

            if replys != None:
                for reply in replys:
                    rid = reply.attr('_rid')
                    # ruser_name = reply.attr('_username')
                    rtext = reply('.ir-content').text()
                    if rid and (rid not in ids):
                        print('回复id：', rid)
                        print('回复内容：', rtext)
                        ids.append(rid)
                        if rid != main_id and rid != host_id:
                            relations.append((host_id, rid))  # 添加评论和评论回复的关系
                            print('回复关系:', host_id, '\t', rid)

    return ids, relations


def file(id_list, relations):
    """
    查重，写入
    :param id_list:
    :param relations:
    :return:
    """
    with open(id_list_file, 'w') as id_txt:
        for id in id_list:
            id_txt.write(str(id) + '\n')

    with open(relation_file, 'w') as re_txt:
        for relation in relations:
            a = id_list.index(relation[0]) + 1
            b = id_list.index(relation[1]) + 1
            print('写入关系:', a, '\t', b)
            re_txt.write(str(a) + '\t' + str(b) + '\n')


def run(key, page):
    """
    :param key:
    :param page:
    :return:
    """
    start_urls = []
    for p in range(page):
        url = 'http://search.tianya.cn/bbs?q={}&pn={}'.format(quote(key), p)
        start_urls.append(url)
    content_urls = prase_all_page(start_urls)
    ids, relations = prase_all_content(content_urls)

    ids_set = set(ids)  # 利用set去重，数据会无序化
    ids = list(ids_set)
    relations_set = set(relations)
    relations = list(relations_set)
    file(ids, relations)


if __name__ == '__main__':
    run(key_word, page)
# urls = ['http://bbs.tianya.cn/post-worldlook-1886395-1.shtml',]
# ids, relations = prase_all_content(urls)
