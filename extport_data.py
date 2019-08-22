#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : extport_data.py
# Create date : 2019-08-22 21:42
# Modified date : 2019-08-22 22:30
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import pymongo

class PoemData:
    def __init__(self):
        conn = pymongo.MongoClient()
        self.db = conn['shici']['data']

    '''导出诗词数据'''
    def export_data(self):
        i = 0
        for item in self.db.find():
            i += 1
            print(i)
            title = item['title'].replace('/','').replace(' ','')
            dynasty = item['dynasty']
            author = item['author']
            tags = ';'.join(item['tags'])
            star = str(item['star'])
            author_stars = str(item['author_stars'])
            content = item['content']
            filename = '-'.join([dynasty, author, title])
            f = open('corpus_poem/%s.txt' % filename, 'w+')
            f.write('dynasty:' + dynasty + '\n')
            f.write('author:' + author + '\n')
            f.write('tags:' + tags + '\n')
            f.write('star:' + star + '\n')
            f.write('author_stars:' + author_stars + '\n')
            f.write('title:' + title + '\n')
            f.write('content:' + content + '\n')
            f.close()
        return


def test():
    handler = PoemData()
    handler.export_data()

test()
