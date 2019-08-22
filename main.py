#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : main.py
# Create date : 2019-08-11 13:41
# Modified date : 2019-08-22 22:30
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

from atm_model import AuthorMining
from poem_process import PoemMining
from poem_spider import PoemSpyder

from location_mining import PoetWalk

def run_spider():
    handler = PoemSpyder()
    handler.author_spider()

def run_author():
    handler = AuthorMining()
    handler.atm_model()
    handler.test_model()
    handler.author_cluster()

def run_poem():
    handler = PoemMining()
    handler.poems_main()
    handler.collect_tags()
    handler.collect_locations()
    handler.collect_author_location()

def run_poet_location():
    name = '李清照'
    handler = PoetWalk()
    handler.mining_main(name)

    name = '苏轼'
    handler = PoetWalk()
    handler.mining_main(name)

    name = '李白'
    handler = PoetWalk()
    handler.mining_main(name)

    name = '文天祥'
    handler = PoetWalk()
    handler.mining_main(name)

    name = '辛弃疾'
    handler = PoetWalk()
    handler.mining_main(name)

    name = '陶渊明'
    handler = PoetWalk()
    handler.mining_main(name)

    name = '李煜'
    handler = PoetWalk()
    handler.mining_main(name)

def run():
    #run_spider()
    run_poem()
    run_author()
    run_poet_location()

run()
