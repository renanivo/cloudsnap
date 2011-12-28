import webapp2

from controllers import *

app = webapp2.WSGIApplication([('/backup', BackupPage),
                               ('/cleanup', CleanupPage)],
                              debug=True)
