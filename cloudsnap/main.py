import webapp2

from handlers import *
from settings import DEBUG


app = webapp2.WSGIApplication([
                               ('/', IndexHandler),
                               ('/backup', BackupHandler),
                               ], debug=DEBUG)
