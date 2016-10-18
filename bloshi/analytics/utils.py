# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from shops.models import Article, Shop, ShopAvailability

from scraping.models import TemporaryItem


def update_article_data(shop, shop_categories=[]):
    if shop_categories:
        articles = Article.objects.filter(shop_category__in=shop_categories)
        temp_items = TemporaryItem.objects.filter(shop_category__in=shop_categories)
    else:
        articles = Article.objects.filter(shop_category__shop=shop)
        temp_items = TemporaryItem.objects.filter(shop_category__shop=shop)
    shop_availabilities = shop.get_shop_availabilities()

    print ">>> >>> ", "%s articles in db..." % len(articles)
    print ">>> >>> ", "%s temporary items in db..." % len(temp_items)

    articles_to_update = []
    articles_to_create = []
    articles_to_set_removed = []

    # Update existing Articles or create a new one
    for item in temp_items:

        if item.shop_availability == '':
            shop_availability = shop_availabilities.get(availability__code=30)
        elif item.shop_availability in shop_availabilities.values_list("keyword", flat=True):
            shop_availability = shop_availabilities.get(keyword=item.shop_availability)
        else:
            shop_availability = shop_availabilities.get(availability__code=30)

        article_list = articles.filter(shop_code=item.shop_code, shop_category=item.shop_category)

        # Too many Articles for update
        if article_list.count() >= 2:
            print ">>> !!! ", "Too many (%s) articles found for shop code %s in shop category %s..." % (
                article_list.count(), item.shop_code, item.shop_category
            )

        # No Articles found, create a new one
        elif article_list.count() == 0:
            article = Article(
                shop_code=item.shop_code,
                shop_category=item.shop_category,
                shop_availability=shop_availability,
                shop_title=item.shop_title,
                shop_url=item.shop_url,
                shop_price=item.shop_price
            )
            articles_to_create.append(article)

        # Update existing Article
        else:
            article = article_list.first()

            article.shop_availability = shop_availability
            article.shop_title = item.shop_title
            article.shop_url = item.shop_url
            article.shop_price = item.shop_price

            articles_to_update.append(article)

    # Set remaining Articles as removed
    shop_availability = shop_availabilities.get(availability__code=40)
    temp_item_shop_codes = temp_items.values_list("shop_code", flat=True)
    for article in articles:
        if article.shop_code not in temp_item_shop_codes:
            article.shop_availability = shop_availability
            articles_to_set_removed.append(article)

    # Bulk updates & creations
    print ">>> >>> ", "Updating articles (%s)..." % len(articles_to_update)
    Article.update_in_bulk(articles_to_update)
    print ">>> >>> ", "Creating new articles (%s)..." % len(articles_to_create)
    Article.create_in_bulk(articles_to_create)
    print ">>> >>> ", "Setting articles as removed (%s)..."  % len(articles_to_set_removed)
    Article.update_in_bulk(articles_to_set_removed)


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