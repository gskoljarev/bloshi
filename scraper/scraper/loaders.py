# -*- coding: utf-8 -*-

import json
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import (
    Identity,
    TakeFirst,
    Join,
    Compose,
    MapCompose,
)


class SpiderItemLoader(ItemLoader):
    FIELDS = ['shop_code', 'shop_title', 'shop_url', 'shop_price', 'shop_availability']

    # Default processors
    default_output_processor = TakeFirst()

    def __init__(self, item=None, selector=None, response=None, parent=None, **context):
        super(SpiderItemLoader, self).__init__(item, selector, response, parent, **context)
        self.db_spider = self.context.get('db_spider')

        # Setup processors
        for field in self.FIELDS:

            # Input
            input_field = str(getattr(self.db_spider, field + '_in'))
            if input_field:
                setattr(self, field + '_in', eval(input_field))

            # Output
            output_field = str(getattr(self.db_spider, field + '_out'))
            if output_field:
                setattr(self, field + '_in', eval(output_field))


    def add_xpaths(self):
        """
        Method for populating item fields from xpaths
        """
        for field in self.FIELDS:
            field_type = getattr(self.db_spider, field + '_type')
            if field_type == 0:
                xpath = str(getattr(self.db_spider, field))
                if xpath:
                    self.add_xpath(field, xpath)

    def add_detail_xpaths(self):
        """
        Method for populating item fields from xpaths after following the item page
        """
        for field in self.FIELDS:
            field_type = getattr(self.db_spider, field + '_type')
            if field_type == 1:
                xpath = str(getattr(self.db_spider, field))
                if xpath:
                    self.add_xpath(field, xpath)

    def add_values(self):
        """
        Method for populating item fields from values
        """
        for field in self.FIELDS:
            field_type = getattr(self.db_spider, field + '_type')
            if field_type == 2:
                value = str(getattr(self.db_spider, field))
                if value:
                    self.add_value(field, value)