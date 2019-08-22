#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : poem_spider.py
# Create date : 2019-08-22 17:41
# Modified date : 2019-08-22 22:31
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import urllib.request
from lxml import etree
import pymongo

class PoemSpyder:
    def __init__(self):
        conn = pymongo.MongoClient()
        self.db = conn['shici']['data']

    '''根据URL请求html'''
    def get_html(self, url):
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        return html

    '''根据诗人进行诗词采集'''
    def author_spider(self):
        #for p_index in range(1, 355):
        for p_index in range(1, 10):
            url = 'https://so.gushiwen.org/authors/default.aspx?p=%s'%p_index
            print(url)
            page = self.get_html(url)
            print(page)
            authors = self.author_parser(page)
            print(authors)
            for tmp in authors:
                id = tmp[0]
                name = tmp[1]
                nums = tmp[2]
                #stars = tmp[3]
                #self.poems_spider(name, id, nums, stars)
                self.poems_spider(name, id, nums)

    '''诗人基本信息解析'''
    def author_parser(self, html):
        selector = etree.HTML(html)
        author_ids = [i.split('_')[1].split('A1.aspx')[0] for i in selector.xpath('//div[@class="cont"]/p[2]/a/@href')]
        #print(author_ids)
        author_names = selector.xpath('//div[@class="divimg"]/a/img/@alt')
        #print(author_names)
        poem_nums = [i.replace('► ', '').replace('篇诗文', '') for i in selector.xpath('//div[@class="cont"]/p[2]/a/text()')]
        #print(poem_nums)

        #stars = [i.replace('\xa0', '') for i in  selector.xpath('//div[@class="good"]/a/span/text()')]
        #print(stars)
        datas = []
        for index, id in enumerate(author_ids):
            try:
                #datas.append([id, author_names[index], poem_nums[index], stars[index]])
                datas.append([id, author_names[index], poem_nums[index]])
            except:
                pass
        return datas

    '''诗词正文采集主函数'''
    #def poems_spider(self, name, id, nums, stars):
    def poems_spider(self, name, id, nums):
        page_nums = int(nums)//10 + 1
        for num in range(1, page_nums + 1):
            url = 'https://so.gushiwen.org/authors/authorvsw.aspx?page={0}&id={1}'.format(num, id)
            print(name, url)
            try:
                html = self.get_html(url)
                #poems = self.poems_extract(html, stars, id)
                poems = self.poems_extract(html, id)
                for data in poems:
                    try:
                        self.db.insert(data)
                    except:
                        pass
            except:
                pass
        return

    '''诗词正文解析'''
    #def poems_extract(self, html, stars, id):
    def poems_extract(self, html, id):
        datas = []
        selector = etree.HTML(html)
        for poem in selector.xpath('//div[@class="sons"]'):
            dynasty = poem.xpath('./div[@class="cont"]/p[2]/a[1]/text()')[0]
            author = poem.xpath('./div[@class="cont"]/p[2]/a[2]/text()')[0]
            title = poem.xpath('./div[@class="cont"]/p[1]/a/b/text()')[0]
            star = poem.xpath('./div[@class="tool"]/div[@class="good"]/a/span/text()')[0]
            content = [i.xpath('string(.)').replace('\n','').replace(' ','') for i in poem.xpath('./div[@class="cont"]/div[@class="contson"]')]
            tags = poem.xpath('./div[@class="tag"]/a/text()')
            data = {}
            data['dynasty'] = dynasty
            data['author'] = author
            data['title'] = title
            data['content'] = ''.join(content)
            data['tags'] = tags
            #data['author_stars'] = int(stars)
            data['star'] = int(star)
            data['id'] = id
            if data:
                datas.append(data)
        return datas

if __name__=='__main__':
    handler = PoemSpyder()
    handler.author_spider()
