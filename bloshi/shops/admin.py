# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html

from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Availability,
    Shop,
    ShopCategory,
    ShopAvailability,
    Article,
)

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Availability)
admin.site.register(Shop)
admin.site.register(ShopCategory)
admin.site.register(ShopAvailability)
admin.site.register(Article)