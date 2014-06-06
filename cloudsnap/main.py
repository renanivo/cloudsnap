import webapp2

from handlers import IndexHandler, BackupHandler
from settings import DEBUG


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/backup', BackupHandler),
    ], debug=DEBUG)
