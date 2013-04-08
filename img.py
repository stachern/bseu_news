from google.appengine.api import images
import webapp2
from models import Article


class BlobImage(webapp2.RequestHandler):

    def get(self):
        if self.request.get("id"):

            article = Article.get_by_id(int(self.request.get("id")))

            if article:
                pic = article.img
                if self.request.get('thumb'):

                    img = images.Image(article.img)

                    width = int(self.request.get('width', 200))
                    height = int(self.request.get('height', img.height * width / img.width))

                    img.resize(height=height, width=width,
                               allow_stretch=False, crop_to_fit=True)
                    img.im_feeling_lucky()
                    pic = img.execute_transforms(output_encoding=images.JPEG)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(pic)
                return

        # Either "id" wasn't provided, or there was no image with that ID in the datastore.
        self.error(404)