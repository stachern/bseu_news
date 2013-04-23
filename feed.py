from models import Article, to_dict
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