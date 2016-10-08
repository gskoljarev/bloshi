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


class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'shop',
        'show_url',
        'shop_code',
        'shop_category',
        'shop_title',
        'shop_availability',
        'shop_price',
        'is_followed',
        'is_listed',
    ]
    list_display_links = ('id', 'show_url',)
    list_filter = (
        'is_followed',
        'is_listed',
        'shop_category__category__code',
        'shop_availability__availability__code',
        'shop_availability__shop__name',
    )
    search_fields = ['id', 'shop_title', 'shop_category__category__code']
    actions = ['set_followed', 'set_listed']


    def set_listed(self, request, queryset):
        for article in queryset:
            article.is_listed = article.is_followed = True
            article.save()
    set_listed.short_description = "Mark selected articles as listed and followed"

    def set_followed(self, request, queryset):
        for article in queryset:
            article.is_followed = True
            article.save()
    set_followed.short_description = "Mark selected articles as followed"

    # Clickable URLs
    def show_url(self, obj):
        return format_html(
            "<a href='{url}'>@</a>",
            url=obj.shop_url,
        )
    show_url.short_description = "URL"


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Availability)
admin.site.register(Shop)
admin.site.register(ShopCategory)
admin.site.register(ShopAvailability)
admin.site.register(Article, ArticleAdmin)