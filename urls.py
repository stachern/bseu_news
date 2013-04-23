import webapp2
import img
import feed
import article

FEED_URLS = [
    webapp2.Route(r'/feed', handler=feed.NewsFeed),
    webapp2.Route(r'/article/<article_id:\d+>', handler=article.EditArticle, name="edit"),
    webapp2.Route(r'/article/', handler=article.AddArticle, name="new")
]

IMG_URLS = [
    webapp2.Route(r'/img', handler=img.BlobImage)
]