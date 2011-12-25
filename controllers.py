import datetime
import webapp2
from boto.ec2.connection import EC2Connection
from boto.exception import EC2ResponseError

from settings import *


class BackupPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        c = EC2Connection(AWS['key'], AWS['secret'], is_secure=SAFE)

        images_created = []

        for reservation in c.get_all_instances():
            for instance in reservation.instances:
                name = "%s-%s" % (datetime.date.today(), instance.id)

                try:
                    image_id = c.create_image(instance.id, name)
                    images_created.append(image_id)
                    message = "%s backed up on image %s" % (instance.id, image_id)
                except EC2ResponseError:
                    message = "Error: %s not backed up" % instance.id

                self.response.out.write(message)

        c.create_tags(images_created,
                      {'created_at': datetime.date.today(),
                       'created_by': 'cloudsnap'});


class CleanupPage(webapp2.RequestHandler):

    def get(self):
        pass
