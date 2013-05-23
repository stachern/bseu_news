from models import Article, to_dict
from handler import BseuEmbedHandler
from datetime import datetime

class NewsFeed(BseuEmbedHandler):

    def get(self):
        """
        Simple offset-based endless json/jsonp feed
        """

        articles = Article.all().filter('publish_state = ', True)\

        if self.request.get('start') and self.request.get('end'):
            articles = articles.filter('publish_date >=',
                                       datetime.strptime(self.request.get('start'), '%d/%m/%Y')
                              ).filter('publish_date <=',
                                       datetime.strptime(self.request.get('end'), '%d/%m/%Y'))

        articles = articles.order('-publish_date').fetch(10, offset=int(self.request.get('offset', 0)))
        articles = [to_dict(item) for item in articles]

        callback = self.request.get('callback')
        if callback:
            self.jsonp_response(articles, callback)
        else:
            self.json_response(articles)