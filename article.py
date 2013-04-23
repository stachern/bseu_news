# coding=utf-8
from google.appengine.ext.db import Blob
from google.appengine.ext.webapp.template import render
import webapp2
from webapp2_extras.appengine.users import admin_required, users
from models import ArticleForm, Article


class AddArticle(webapp2.RequestHandler):

    @admin_required
    def get(self, *args, **kwargs):
        msg = []
        if self.request.get('message'):
            msg.append({'text': self.request.get('message')})
        self.response.out.write(render('templates/article.html', {'form': ArticleForm(),
                                                                  'url': '/article/',
                                                                  'user': users.get_current_user(),
                                                                  'messages': msg}))

    def post(self):
        article = self.request.POST.get('id')
        instance = Article.get(article) if article else None

        data = ArticleForm(data=self.request.POST, instance=instance)
        if data.is_valid():
            entity = data.save(commit=False)
            if hasattr(self.request.POST.get('img'), 'file'):
                entity.img = Blob(self.request.POST.get('img').file.read())
            entity.put()
            self.redirect_to("new", message='Статья успешно сохранена!')
        else:
            self.response.out.write(render('templates/article.html', {'form': data}))


class EditArticle(webapp2.RequestHandler):

    @admin_required
    def get(self, article_id):
        article = Article.get_by_id(int(article_id))
        data = ArticleForm(instance=article)
        self.response.out.write(render('templates/article.html', {'form': data,
                                                                  'url': '/article/',
                                                                  'id': article.key()}))