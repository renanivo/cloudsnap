import webapp2
from ec2adapters import EC2Account
from boto.exception import EC2ResponseError
from logger import Logger


class BackupHandler(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        account = EC2Account()

        for instance in account.get_instances():
            try:
                image_id = account.backup_instance(instance)
                message = "%s backed up on image %s" % (instance.id, image_id)
            except EC2ResponseError:
                message = "Error: %s not backed up" % instance.id

            Logger.log(self, message)
