import webapp2
from boto.ec2.connection import EC2Connection

from settings import *

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        connection = EC2Connection(AWS['key'],
                                   AWS['secret'],
                                   is_secure=SAFE)

        instances = connection.get_all_instances()
        self.response.out.write(instances)

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
