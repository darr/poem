#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : location_mining.py
# Create date : 2019-08-22 21:43
# Modified date : 2019-08-22 22:30
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

from urllib import request
from lxml import etree
from urllib import parse
from sentence_parser import *
import json
import page

class PoetWalk:
    def __init__(self):
        self.name_dict = {i.strip().split(',')[0]:i.strip().split(',')[2:] for i in open('./data/city_map.txt') if len(i.strip().split(',')) == 5}
        self.base = page.page_base

    '''请求数据'''
    def get_html(self, url):
        return request.urlopen(url).read().decode('utf-8')

    '''获取诗人生平事迹'''
    def extract_desc(self, word):
        url = "http://baike.baidu.com/item/%s" % parse.quote(word)
        #print(url)
        html = self.get_html(url)
        content = [i for i in html.split('<h2 class="title-text">') if word + '</span>人物生平</h2>' in i]
        selector = etree.HTML(content[0])

        # content = html
        # selector = etree.HTML(content)

        res = [i.xpath('string(.)').replace('\n','').replace('\xa0','') for i in selector.xpath('//div[@class="para"]')]
        desc = ''.join([i for i in res if i])
        return desc

    '''基于生平事迹，挖掘诗人关联地点'''
    def collect_locations(self, name):
        content = self.extract_desc(name)
        handler = LtpParser()
        locations = handler.collect_locations(content)
        if not locations:
            return []
        else:
            locations = [self.transfer_location(i) for i in set(locations)]
        locations =[i for i in locations if i]
        #print(locations)
        return locations

    '''基于地点，进行古今地点的转换'''
    def transfer_location(self, loc):
        geo_info = self.name_dict.get(loc, 'na')
        if geo_info != 'na':
            return [loc] + geo_info
        else:
            tmp = self.get_abs_geo(loc)
            #print(tmp)
            if not tmp:
                return []
            else:
                return tmp

    '''调用远程api，获取绝对经纬度'''
    def get_abs_geo(self, word):
        url = 'https://apis.map.qq.com/jsapi?qt=poi&wd='+parse.quote(word)
        print(url)
        data = request.urlopen(url).read().decode('gbk')
        data_json = json.loads(data)
        name = ''
        lon = 0
        lat = 0
        if 'pois' in data_json['detail']:
            if len(data_json['detail']['pois']) > 0:
                city_info = data_json['detail']['pois'][0]
                name = word
                lon = str(city_info['pointx'])
                lat = str(city_info['pointy'])
        else:
            if 'city' in data_json['detail']:
                city_info = data_json['detail']['city']
                lon = str(city_info['pointx'])
                lat = str(city_info['pointy'])
                name = city_info['cname']

        if name == '全国':
            return []
        if name and lon and lat:
            return [word, name, lat, lon]
        else:
            return []

    '''挖掘主函数'''
    def mining_main(self, name):
        locations = self.collect_locations(name)
        self.create_html(name, locations)

    '''传入地点数据，绘制足迹地图'''
    def create_html(self, name, locations):
        datas = ''
        for loc in locations:
            if '国' not in loc[1]:
                body = "{name:"+ "'{0}', lat:{1}, lon:{2}".format(loc[1], loc[2], loc[3]) + "},\n"
                datas += body.replace('"','')

        html = self.base.replace('target_datas', datas).replace('author', name + '足迹地图')
        f = open('./output/{0}.html'.format(name), 'w+')
        f.write(html)
        f.close()
        return

def test():
    name = '李清照'
    handler = PoetWalk()
    handler.mining_main(name)

#test()
