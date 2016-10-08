# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from model_utils import Choices

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from shops.models import Shop


@python_2_unicode_compatible
class Spider(models.Model):
    TYPE = Choices(
        (0, 'list', _('list')),
        (1, 'detail', _('detail')),
        (2, 'custom', _('custom')),
    )

    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, null=True, blank=True)
    parse_detailed_info = models.BooleanField(_('Parse detailed info?'), default=False)
    initial_request_url = models.URLField(_('Initial request URL'), blank=True)

    next_page_xpath = models.TextField(_('Next page XPath'), blank=True)
    selector_xpath = models.TextField(_('Selector XPath'), blank=True)

    shop_code_type = models.IntegerField(choices=TYPE, default=TYPE.list)
    shop_code = models.TextField(_('code'), blank=True)
    shop_code_in = models.TextField(_('code input'), blank=True)
    shop_code_out = models.TextField(_('code output'), blank=True)

    shop_title_type = models.IntegerField(choices=TYPE, default=TYPE.list)
    shop_title = models.TextField(_('shop_title'), blank=True)
    shop_title_in = models.TextField(_('shop_title input'), blank=True)
    shop_title_out = models.TextField(_('shop_title output'), blank=True)

    shop_url_type = models.IntegerField(choices=TYPE, default=TYPE.list)
    shop_url = models.TextField(_('url'), blank=True)
    shop_url_in = models.TextField(_('url input'), blank=True)
    shop_url_out = models.TextField(_('url output'), blank=True)

    shop_price_type = models.IntegerField(choices=TYPE, default=TYPE.list)
    shop_price = models.TextField(_('price'), blank=True)
    shop_price_in = models.TextField(_('price input'), blank=True)
    shop_price_out = models.TextField(_('price output'), blank=True)

    shop_availability_type = models.IntegerField(choices=TYPE, default=TYPE.list)
    shop_availability = models.TextField(_('shop_availability'), blank=True)
    shop_availability_in = models.TextField(_('shop_availability input'), blank=True)
    shop_availability_out = models.TextField(_('shop_availability output'), blank=True)


    def __str__(self):
        return "%s spider" % self.shop.name

    class Meta:
        db_table = 'spiders'
        verbose_name = 'Spider'
        verbose_name_plural = 'Spiders'