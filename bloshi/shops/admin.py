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


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['id', 'code', 'name']


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']


class ShopCategoryInline(admin.TabularInline):
    model = ShopCategory


class ShopAvailabilityInline(admin.TabularInline):
    model = ShopAvailability


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'url']
    inlines = (ShopCategoryInline, ShopAvailabilityInline,)


class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'category', 'url']


class ShopAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'keyword', 'availability']


class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'shop',
        'show_url',
        'shop_code',
        'shop_category',
        'shop_title',
        'colored_shop_availability',
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
    actions = [
        'set_followed',
        'set_listed_followed',
        'set_unlisted',
        'set_unfollowed',
    ]


    def set_listed_followed(self, request, queryset):
        for article in queryset:
            article.is_listed = article.is_followed = True
            article.save()
    set_listed_followed.short_description = "Mark selected articles as listed and followed"

    def set_followed(self, request, queryset):
        for article in queryset:
            article.is_followed = True
            article.save()
    set_followed.short_description = "Mark selected articles as followed"

    def set_unlisted(self, request, queryset):
        for article in queryset:
            article.is_listed = False
            article.save()
    set_unlisted.short_description = "Mark selected articles as unlisted"

    def set_unfollowed(self, request, queryset):
        for article in queryset:
            article.is_followed = False
            article.save()
    set_unfollowed.short_description = "Mark selected articles as unfollowed"

    # Clickable URLs
    def show_url(self, obj):
        return format_html(
            "<a href='{url}'>@</a>",
            url=obj.shop_url,
        )
    show_url.short_description = "URL"

    def colored_shop_availability(self, obj):
        if obj.shop_availability.availability.code == 10:
            return format_html(
                '<span style="color: #{};">{}</span>',
                "009900",
                obj.shop_availability,
            )
        return obj.shop_availability


admin.site.register(Category, CategoryAdmin)
admin.site.register(Availability, AvailabilityAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(ShopCategory, ShopCategoryAdmin)
admin.site.register(ShopAvailability, ShopAvailabilityAdmin)
admin.site.register(Article, ArticleAdmin)