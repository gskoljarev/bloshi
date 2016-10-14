# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Spider, TemporaryItem


class SpiderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'shop'
    ]

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={
                    'rows': 1,
                    'cols': 140,
                    'style': 'font-family: Monospace'
                }
            )
        },
    }


class TemporaryItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'shop',
        'shop_code',
        'shop_category',
        'shop_title',
        'shop_availability',
        'shop_price',
    ]
    list_filter = (
        'shop_category__category__code',
        'shop_availability',
    )

admin.site.register(Spider, SpiderAdmin)
admin.site.register(TemporaryItem, TemporaryItemAdmin)