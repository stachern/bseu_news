import webapp2
import urls

feed_app = webapp2.WSGIApplication(urls.FEED_URLS, debug=True)
img_app = webapp2.WSGIApplication(urls.IMG_URLS, debug=True)