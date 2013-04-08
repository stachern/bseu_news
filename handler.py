import datetime
from urlparse import urlsplit, urlunsplit
import webapp2
import json


class JSONResponseHandler(webapp2.RequestHandler):

    def _get_json(self, data):
        date_handler = lambda obj: obj.isoformat() if isinstance(obj, (datetime.datetime, datetime.date)) else None
        return json.dumps(data,  default=date_handler)

    def json_response(self, data):
        self.response.headers['Content-Type'] = 'json'
        self.response.out.write(self._get_json(data))

    def jsonp_response(self, data, callback):
        self.response.headers['Content-Type'] = 'application/javascript'
        self.response.out.write('%s(%s);' % (callback, self._get_json(data)))


class BseuEmbedHandler(JSONResponseHandler):

    def __getattribute__(self, name):
        attr = super(BseuEmbedHandler, self).__getattribute__(name)
        if hasattr(attr, '__call__') and name in ['get', 'post']:
            # noinspection PyBroadException
            def add_header(*args, **kwargs):
                self.response.headers['Content-Type'] = 'json'  # default
                try:
                    referrer = urlsplit(self.request.referer)
                    access_control = urlunsplit((referrer.scheme, referrer.netloc, '', '', ''))
                except Exception, e:
                    access_control = '*'
                self.response.headers['Access-Control-Allow-Origin'] = access_control

                return attr(*args, **kwargs)

            return add_header
        else:
            return attr


