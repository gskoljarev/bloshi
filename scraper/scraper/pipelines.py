# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scraping.models import TemporaryItem


class ScraperPipeline(object):
    def __init__(self):
        self.itemset = []

    def process_item(self, item, spider):
        # Create item instance, do not write to db but add to list
        item.save(commit=False)
        self.itemset.append(item.instance)
        return item

    def close_spider(self, spider):
        print ">>> ", "Saving temporary items to db..."
        TemporaryItem.create_in_bulk(self.itemset)
        print ">>> ", "Temporary items saved in db."
