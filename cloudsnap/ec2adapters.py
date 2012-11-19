import datetime

from boto.ec2.connection import EC2Connection

from settings import AWS, AMI_NAME_TEMPLATE
from plus import log_method


class EC2Account():

    def __init__(self, connection=None):
        if connection is None:
            self._connection = EC2Connection(
                    AWS['key'],
                    AWS['secret'],
                    is_secure=AWS['use_safe_connection']
                    )
        else:
            self._connection = connection

    def _create_AMI_name(self, instance):
        if "Name" in instance.tags:
            name = instance.tags["Name"]
        else:
            name = instance.id

        return AMI_NAME_TEMPLATE % {"today": datetime.date.today(),
                                   "name": name,
                                   "instance_id": instance.id,
                                   }

    @log_method
    def get_instances(self):
        """Return a list of all EC2 instances of the account"""
        instances = []

        for reservation in self._connection.get_all_instances():
            for instance in reservation.instances:
                instances.append(instance)

        return instances

    @log_method
    def backup_instance(self, instance):
        """Create a backup (AMI) of a given instance"""
        image_id = self._connection.create_image(
                    instance.id,
                    self._create_AMI_name(instance)
                    )
        self._connection.create_tags([image_id],
                                     {'instance': instance.id,
                                      'created_at': datetime.date.today(),
                                      'created_by': 'cloudsnap',
                                      })
        return image_id

    @log_method
    def get_backups(self):
        """Return a list of all backups (AMIs) created by it"""
        return self._connection.get_all_images(
                filters={"tag:created_by": u"cloudsnap"}
                )

    @log_method
    def delete_backup(self, image):
        """Delete a backup (AMI)"""
        self._connection.deregister_image(image.id, True)
