"""
    ！！！如果要获取全部图片  则开始前 需要先注释  117 行的 break
"""
import requests
from urllib.parse import urljoin
from parsel import Selector
import os
import random
import json
import time
from multiprocessing.dummy import Pool

UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"
]



def get_album_url(keyword,page_num):
    """

    :param keyword: 该网站的标签 关键字
    :param page_num:  设置的下载页数  实际的页数是 page_num-1    比如 page_name = 2  实际只有一页
    :return:
    """
    ua = random.choice(UserAgent_List)
    header = {
        'User-Agetn':ua
    }
    # range 要从1开始  不设置默认是0  这里有点坑
    for num in range(1,page_num):
        json_api = 'https://tuchong.com/rest/tags/%s/posts?page=%s&count=20&order=weekly' %(keyword,num)
        response = requests.get(json_api,headers=header)
        response.encoding = 'utf-8'
        data = json.loads(response.text)
        print('第  %s  页 的图集数量:%s' %(num,len(data['postList'])))
        writed_num = 0
        for mm in data['postList']:
            url = mm['url']
            get_image_url(url)
            writed_num += 1
            print('第  %s  页 写入进度:%s / %s' %(num,writed_num,len(data['postList'])))
    print('第  %s  页 写入完成' %num)


def get_image_url(url):
    """
    获取 图集下的所有图片链接  并 保存图片到不同的文件夹下
    :param url: 传入的是 图集的url
    :return:
    """
    # url = 'https://tuchong.com/1058467/16833620/'
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = Selector(response.text)

    album_title_status = html.xpath('//h1[@class="post-title"]/text()').extract()
    if album_title_status:
        album_title = album_title_status[0]
    else:
        album_title = url[-17:]

    img_list = html.xpath('//article[@class="post-content"]/img/@src').extract()
    len(img_list)

    page_count = 0
    # 下载并保存原图
    if img_list :
        for img_url in img_list:
            ua = random.choice(UserAgent_List)
            header = {
                'User-Agent': ua
            }
            res = requests.get(img_url,headers=header)

            path = os.path.abspath('.') + '\\图虫图集\\' + album_title + '\\'
            if not os.path.exists(path):
                os.makedirs(path)
            file = path + img_url[-12:]
            # print(file)
            with open(file,'wb') as f :
                f.write(res.content)
                page_count += 1
                print('{} 进度: {} / {}'.format(album_title,page_count,len(img_list)))
            break

        print('%s  **********写入完成**********' % album_title)
    else:
        print('%s    -------->此图集为空或者格式不一样' %album_title)

def get_tags_list():
    url = 'https://tuchong.com/explore/'
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = Selector(response.text)
    tags_list = html.xpath('//div[@class="page-content"]/div/ul/li/a/img/@alt').extract()
    print(tags_list)

def test_get_album_url():
    key = '美女'
    page_num = 5
    get_album_url(key,page_num)

def test_get_image_url():
    url = 'https://tuchong.com/1058467/16833620/'
    get_image_url(url)

def main():
    """
    程序开始前要设置 keyword  和 page_num  不然就会使用默认的设置
    :return:
    """
    keywords = '美女'    #标签关键字
    page_num = 10      #异步加载的页数 不能小于1
    get_album_url(keywords,page_num)

# base_url = 'https://tuchong.com/explore/'
# url = 'https://tuchong.com/tags/%E7%BE%8E%E5%A5%B3/'
# api = 'https://tuchong.com/rest/tags/%E7%BE%8E%E5%A5%B3/posts?page=3&count=20&order=weekly'

if __name__=='__main__':
    main()
    # thread_pool = Pool(3)
    # thread_pool.map(main(),)

    # get_tags_list()
