import webapp2

from handlers import *

app = webapp2.WSGIApplication([('/', IndexHandler),
                               ('/backup', BackupHandler),
                               ('/cleanup', CleanupHandler)],
                              debug=True)
