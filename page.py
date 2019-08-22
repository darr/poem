#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : page.py
# Create date : 2019-08-22 16:21
# Modified date : 2019-08-22 22:31
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

page_base = '''
              <!DOCTYPE HTML>
               <html>
                   <head>
                       <meta charset="utf-8"><link rel="icon" href="https://static.jianshukeji.com/highcharts/images/favicon.ico">
                       <meta name="viewport" content="width=device-width, initial-scale=1">
                       <script src="https://img.hcharts.cn/jquery/jquery-1.8.3.min.js"></script>
                       <script src="https://img.hcharts.cn/highmaps/highmaps.js"></script>
                       <script src="https://cdnjs.cloudflare.com/ajax/libs/proj4js/2.3.6/proj4.js"></script>
                   </head>
                   <body>
                       <div id="container" style=" height: 1000px"></div>
                       <script src="https://data.jianshukeji.com/geochina/china.js"></script>
                       <script>
                           var data = [
                                   target_datas
                                   ];

                           var map = new Highcharts.Map('container', {
                               title: {
                                   text: 'author'
                               },
                               mapNavigation: {
                                   enabled: true,
                                   buttonOptions: {
                                       verticalAlign: 'bottom'
                                   }
                               },
                               tooltip: {
                                   useHTML: true,
                                   formatter: function() {
                                       return this.point.name;
                                   }
                               },
                               plotOptions: {
                                   series: {
                                       dataLabels: {
                                           enabled: true
                                       },
                                       marker: {
                                           radius: 3
                                       }
                                   }
                               },
                               series: [{
                                   // 空数据列，用于展示底图
                                   mapData: Highcharts.maps['cn/china'],
                                   showInLegend: false
                               },{
                                   type: 'mappoint',
                                   name: 'author',
                                   data: data
                               }]
                           });
                       <!--});-->
                       </script>
                   </body>
               </html>
               '''
