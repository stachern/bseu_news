from google.appengine.ext.db import Blob
from google.appengine.ext.webapp.template import render
import webapp2
from webapp2_extras.appengine.users import admin_required
from models import ArticleForm, Article, to_dict
from handler import BseuEmbedHandler


class NewsFeed(BseuEmbedHandler):

    def get(self):
        """
        Simple offset-based endless json/jsonp feed
        """

        articles = Article.all().order('-publish_date').filter('publish_state = ',
                                                               True).fetch(10,
                                                                           offset=int(self.request.get('offset', 0)))
        articles = [to_dict(item) for item in articles]

        callback = self.request.get('callback')
        if callback:
            self.jsonp_response(articles, callback)
        else:
            self.json_response(articles)


class AddArticle(webapp2.RequestHandler):

    @admin_required
    def get(self):
        self.response.out.write(render('templates/AddArticle.html', {'form': ArticleForm().as_table(),
                                                                     'url': '/article/'}))

    def post(self):
        article = self.request.POST.get('id')
        instance = Article.get(article) if article else None

        data = ArticleForm(data=self.request.POST, instance=instance)
        if data.is_valid():
            entity = data.save(commit=False)
            if hasattr(self.request.POST.get('img'), 'file'):
                entity.img = Blob(self.request.POST.get('img').file.read())
            entity.put()
            self.response.out.write('<script>window.close();</script>')
        else:
            self.response.out.write(render('templates/AddArticle.html', {'form': data.as_table()}))


class EditArticle(webapp2.RequestHandler):

    @admin_required
    def get(self, article_id):
        article = Article.get_by_id(int(article_id))
        data = ArticleForm(instance=article)
        self.response.out.write(render('templates/AddArticle.html', {'form': data.as_table(),
                                                                     'url': '/article/',
                                                                     'id': article.key()}))