# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(_('Name'), max_length=50, unique=True)
    code = models.CharField(_('Code'), max_length=7, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return "%s" % self.code

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


@python_2_unicode_compatible
class Availability(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    code = models.IntegerField(_('Code'))

    def __str__(self):
        return "%s" % self.code

    class Meta:
        db_table = 'availabilities'
        verbose_name = 'Availability'
        verbose_name_plural = 'Availabilities'


@python_2_unicode_compatible
class Shop(models.Model):
    name = models.CharField(_('Name'), max_length=50, blank=True)
    code = models.CharField(_('Code'), max_length=3, blank=True)
    url = models.URLField(_('URL'), blank=True)
    categories = models.ManyToManyField(Category, through="ShopCategory")
    availabilities = models.ManyToManyField(Availability, through="ShopAvailability")

    def __str__(self):
        return "%s" % self.name

    class Meta:
        db_table = 'shops'
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    def get_shop_categories(self):
        return self.shopcategory_set.all()

    def get_shop_availabilities(self):
        return self.shopavailability_set.all()


@python_2_unicode_compatible
class ShopCategory(MPTTModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField(_('Name'), max_length=50, blank=True)
    url = models.URLField(_('URL'), blank=True)

    def __str__(self):
        return "%s" % self.category

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'shopcategories'
        verbose_name = 'Shop category'
        verbose_name_plural = 'Shop categories'


@python_2_unicode_compatible
class ShopAvailability(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    keyword = models.CharField(_('Keyword'), max_length=50, blank=True)

    def __str__(self):
        return "%s" % self.availability

    class Meta:
        db_table = 'shopavailabilities'
        verbose_name = 'Shop availability'
        verbose_name_plural = 'Shop availabilities'


@python_2_unicode_compatible
class Article(models.Model):
    shop_category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE)
    shop_availability = models.ForeignKey(ShopAvailability, on_delete=models.CASCADE)
    shop_code = models.CharField(_('Shop code'), max_length=20, blank=True)
    shop_title = models.CharField(_('Shop title'), max_length=255, blank=True)
    search_title = models.CharField(_('Search title'), max_length=255, blank=True)
    title = models.CharField(_('Title'), max_length=255, blank=True)
    shop_url = models.URLField(_('Shop URL'), blank=True)
    shop_price = models.DecimalField(_('Shop price'), max_digits=7, decimal_places=2, default=0.00)
    is_listed = models.BooleanField(_('Is listed?'), default=False)
    is_followed = models.BooleanField(_('Is followed?'), default=False)
    # image = ImageField()

    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return "%s" % self.shop_title

    @classmethod
    def create_in_bulk(cls, articles):
        cls.objects.bulk_create(articles)

    @classmethod
    def update_in_bulk(cls, articles):
        from bulk_update.helper import bulk_update
        bulk_update(
            articles,
            exclude_fields=['shop_code','shop_category'],
            batch_size=100
        )

    @property
    def shop(self):
        return self.shop_category.shop.code

    @property
    def truncated_url(self):
        return truncatechars(self.url, 10)