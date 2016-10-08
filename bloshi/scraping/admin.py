# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Spider


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

admin.site.register(Spider, SpiderAdmin)