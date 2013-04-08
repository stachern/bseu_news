import webapp2
import img
import feed

FEED_URLS = [
    webapp2.Route(r'/feed', handler=feed.NewsFeed),
    webapp2.Route(r'/article/<article_id:\d+>', handler=feed.EditArticle),
    webapp2.Route(r'/article/', handler=feed.AddArticle)
]

IMG_URLS = [
    webapp2.Route(r'/img', handler=img.BlobImage)
]