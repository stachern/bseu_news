#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from google.appengine.ext import db
import djangoforms

SIMPLE_TYPES = (int, long, float, bool, dict, basestring)


def to_dict(model):
    output = {}

    for key, prop in model.properties().iteritems():

        value = getattr(model, key)

        # TODO: get rid of key hardcode
        if key == 'img':
            if not value is None:
                output[key] = {'id': str(model.key().id())}
            continue

        if isinstance(value, list):
            if isinstance(value[0], db.Key):
                output[key.kind()] = [to_dict(db.get(key)) for key in value]
            else:
                output[key] = value
        elif value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            output[key] = value.isoformat()
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output


class Article(db.Model):
    creation_date = db.DateTimeProperty(auto_now_add=True, verbose_name='Дата создания', required=True)
    publish_date = db.DateProperty(verbose_name='Дата начала публикации', required=True)
    header = db.StringProperty(verbose_name='Заголовок новости', required=True)
    body = db.TextProperty(verbose_name='Текст новости', required=True)
    img = db.BlobProperty(verbose_name='Картинка к новости')
    publish_state = db.BooleanProperty(verbose_name='Показывать на сайте', default=True)
    is_monthphrase = db.BooleanProperty(verbose_name='Показывать дату', default=False)


class ArticleForm(djangoforms.ModelForm):
    class Meta:
        model = Article
