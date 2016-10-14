# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scraping.models import TemporaryItem
from analytics.utils import update_article_data


class ScraperPipeline(object):
    def __init__(self):
        self.itemset = []

    def process_item(self, item, spider):
        # Create item instance, do not write to db but add to list
        item.save(commit=False)
        self.itemset.append(item.instance)
        return item

    def close_spider(self, spider):
        print ">>> ", "Parsed %s items..." % len(self.itemset)
        if spider.save == True:
            print ">>> ", "Clear existing temporary items in db..."
            TemporaryItem.objects.all().delete()
            print ">>> ", "Saving temporary items to db..."
            TemporaryItem.create_in_bulk(self.itemset)
            print ">>> ", "Temporary items saved in db..."
            print ">>> ", "Saving article data..."
            update_article_data(spider.shop, spider.shop_categories)
            print ">>> ", "Article data saved!"
