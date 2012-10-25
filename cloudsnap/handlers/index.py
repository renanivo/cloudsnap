import webapp2


class IndexHandler(webapp2.RequestHandler):

    def get(self):
        return webapp2.redirect("https://github.com/renanivo/cloudsnap")
