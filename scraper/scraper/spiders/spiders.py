# -*- coding: utf-8 -*-

import scrapy

from scraper.items import TemporaryItem
from scraper.loaders import SpiderItemLoader

from shops.models import Shop
from scraping.models import Spider


class DBSpider(scrapy.Spider):
    name = 'spider'

    def __init__(self, shop=None, category=None, exclude_category=None, save=True, **kwargs):
        self.item = TemporaryItem
        self.item_loader = SpiderItemLoader
        # Load spider params
        self.category = category
        self.exclude_category = exclude_category
        self.save = save
        # Load needed shop data
        self.shop = Shop.objects.get(code=shop)
        self.shop_availabilities = self.shop.get_shop_availabilities()
        # Load scraping data
        self.db_spider = self.shop.spider
        self.initial_request_url = str(self.db_spider.initial_request_url)
        self.parse_detailed_info = self.db_spider.parse_detailed_info

    def start_requests(self):
        # Initial request
        if self.initial_request_url:
            yield scrapy.Request(url=self.initial_request_url)

        self.shop_categories = self.shop.get_shop_categories()
        if self.exclude_category:
            self.shop_categories = self.shop_categories.exclude(category__code=self.exclude_category)
        if self.category:
            self.shop_categories = self.shop_categories.filter(category__code=self.category)

        for shop_category in self.shop_categories:
            yield scrapy.Request(
                url=shop_category.url,
                dont_filter=True,
                meta={
                    'shop_category': shop_category
                }
            )

    def parse_details(self, response):
        l = response.meta['item_loader']
        l.selector = l.default_selector_class(response)
        l.response = response

        l.add_detail_xpaths()
        yield l.load_item()

    def parse(self, response):
        details_requests = []
        for sel in response.xpath(str(self.db_spider.selector_xpath)):
            l = self.item_loader(item=self.item(), selector=sel, db_spider=self.db_spider)
            l.add_xpaths()
            l.add_values()
            l.add_value(
                'shop_category',
                response.meta['shop_category']
            )
            l.load_item()

            # Parse details page and extract rest of needed fields
            if self.parse_detailed_info == True:
                details_requests.append(
                    scrapy.Request(
                        url=l.item['url'],
                        callback=self.parse_details,
                        meta={'item_loader': l}
                    )
                )
            else:
                yield l.load_item()

        for request in details_requests:
            yield request

        # Go to next page
        if self.db_spider.next_page_xpath:
            next_page = response.xpath(str(self.db_spider.next_page_xpath)).extract()

            # HACK AHEAD!
            if next_page != [u''] and next_page != []:
                next_page= next_page[0]
                # Manually create next page urls from page numbers
                if self.db_spider.next_page_is_calc:
                    next_page_num = next_page
                    url = response.url[:-1] + next_page_num  # This line relies on URL having page param at the end (...&page=3)
                # Full next page URL
                else:
                    url = response.urljoin(next_page)

                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={
                        'shop_category': response.meta['shop_category']
                    }
                )