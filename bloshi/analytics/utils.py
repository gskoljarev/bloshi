# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from shops.models import Article, Shop, ShopAvailability

from scraping.models import TemporaryItem


def update_article_data(shop):
    articles = Article.objects.all()
    temp_items = TemporaryItem.objects.all()
    shop_availabilities = shop.get_shop_availabilities()

    articles_to_update = []
    articles_to_create = []

    for item in temp_items:
        # Update existing Article instance or create a new one
        try:
            article = articles.get(
                shop_code=item.shop_code, shop_category=item.shop_category
            )
            if item.shop_availability == '':
                article.shop_availability = shop_availabilities.get(availability__code=30)
            elif item.shop_availability in shop_availabilities.values_list("keyword", flat=True):
                article.shop_availability = shop_availabilities.get(keyword=item.shop_availability)
            else:
                article.shop_availability = shop_availabilities.get(availability__code=40)

            article.shop_title = item.shop_title
            article.shop_url = item.shop_url
            article.shop_price = item.shop_price

            articles_to_update.append(article)
        except:
            if item.shop_availability in shop_availabilities.values_list("keyword", flat=True):
                shop_availability = shop_availabilities.get(keyword=item.shop_availability)
            else:
                shop_availability = shop_availabilities.get(availability__code=40)
            article = Article(
                shop_code=item.shop_code,
                shop_category=item.shop_category,
                shop_availability=shop_availability,
                shop_title=item.shop_title,
                shop_url=item.shop_url,
                shop_price=item.shop_price
            )
            articles_to_create.append(article)

    # Bulk updates & creations
    print ">>> ", "Updating articles (%s)..." % len(articles_to_update)
    Article.update_in_bulk(articles_to_update)
    print ">>> ", "Creating new articles (%s)..." % len(articles_to_create)
    Article.create_in_bulk(articles_to_create)


def update_article_data_slow(shop):
    articles = Article.objects.all()
    temp_items = TemporaryItem.objects.all()
    shop_availabilities = shop.get_shop_availabilities()

    articles_to_update = []
    articles_to_create = []

    for item in temp_items:
        article_fields = {}

        if item.shop_availability in shop_availabilities.values_list("keyword", flat=True):
            article_fields["shop_availability"] = shop_availabilities.get(keyword=item.shop_availability)
        else:
            article_fields["shop_availability"] = shop_availabilities.get(
                availability__code=40)

        article_fields["shop_title"] = item.shop_title
        article_fields["shop_url"] = item.shop_url
        article_fields["shop_price"] = item.shop_price

        obj, created = Article.objects.update_or_create(
            shop_code=item.shop_code, shop_category=item.shop_category, defaults=article_fields)