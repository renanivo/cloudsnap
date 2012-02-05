import datetime

import webapp2
from boto.ec2.connection import EC2Connection
from boto.exception import EC2ResponseError

from logger import Logger
from settings import *
from shortcuts import get_all_instances, create_instance_backup_name

class IndexHandler(webapp2.RequestHandler):

    def get(self):
        return webapp2.redirect("https://github.com/renanivo/cloudsnap")


class BackupHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        c = EC2Connection(AWS['key'], AWS['secret'], is_secure=SAFE)

        for instance in get_all_instances(c):
            name = create_instance_backup_name(AMI_NAME_TEMPLATE, instance)

            try:
                image_id = c.create_image(instance.id, name)
                message = "%s backed up on image %s" % (instance.id, image_id)

                c.create_tags([image_id],
                              {'instance': instance.id,
                               'created_at': datetime.date.today(),
                               'created_by': 'cloudsnap'});
            except EC2ResponseError:
                message = "Error: %s not backed up" % instance.id

            Logger.log(self, message)


class CleanupHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        c = EC2Connection(AWS['key'], AWS['secret'], is_secure=SAFE)

        for image in c.get_all_images():
            if (image.tags.has_key('created_by') and
                image.tags['created_by'] == 'cloudsnap' and
                image.tags['created_at'] != str(datetime.date.today())):
                c.deregister_image(image.id, True)
                Logger.log(self, "image %s deregistered and snapshot %s deleted" %
                                  (image.id, image.block_device_mapping.current_value.snapshot_id))
