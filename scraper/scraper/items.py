# -*- coding: utf-8 -*-

from scrapy_djangoitem import DjangoItem
from scraping.models import TemporaryItem


class TemporaryItem(DjangoItem):
    django_model = TemporaryItem
