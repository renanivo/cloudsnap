import datetime

import webapp2
from boto.exception import EC2ResponseError

from logger import Logger
from ec2adapters import EC2Account
from filters import filter_backups_by_tags


class IndexHandler(webapp2.RequestHandler):

    def get(self):
        return webapp2.redirect("https://github.com/renanivo/cloudsnap")


class BackupHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        account = EC2Account()

        for instance in account.get_instances():
            try:
                image_id = account.backup_instance(instance)
                message = "%s backed up on image %s" % (instance.id, image_id)
            except EC2ResponseError:
                message = "Error: %s not backed up" % instance.id

            Logger.log(self, message)


class CleanupHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        account = EC2Account()

        today = str(datetime.date.today())
        backups = account.get_backups()
        old_backups = filter_backups_by_tags(backups,
                                             tags_equal={"created_by":
                                                         "cloudsnap"},
                                             tags_not_equal={"created_at":
                                                             today}
                                             )
        print old_backups

        for backup in old_backups:
            account.delete_backup(backup)
            Logger.log(self,
                       "image %s deregistered and snapshot %s deleted" %
                       (backup.id,
                        backup.block_device_mapping.current_value.snapshot_id))
