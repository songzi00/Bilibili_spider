# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os


class BCommentPipeline(object):
    def process_item(self, item, spider):
        return item


class Pipeline_ToCSV(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/spiders/yzsy.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'wb')
        # csv写法
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        if item['time']:  #str(b, encoding = "utf8")
            self.writer.writerow((str(item['time']), str(item['content'])))
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()


