import datetime

import jinja2
from boto.ec2.connection import EC2Connection

from settings import AWS, AMI_NAME_TEMPLATE
from filters import filter_backups_by_tags


class EC2Account():

    def __init__(self, connection=None):
        if connection is None:
            self._connection = EC2Connection(AWS['key'],
                                             AWS['secret'],
                                             is_secure=AWS['use_safe_connection'])
        else:
            self._connection = connection

    def _create_AMI_name(self, instance):
        env = jinja2.Environment()
        template = env.from_string(AMI_NAME_TEMPLATE)

        name = instance.tags["Name"] if instance.tags.has_key("Name") else instance.id

        return template.render({
            "today": datetime.date.today(),
            "name": name,
            "instance_id": instance.id,
            })

    def get_instances(self):
        """Return a list of all EC2 instances of the account"""
        instances = []

        for reservation in self._connection.get_all_instances():
            for instance in reservation.instances:
                instances.append(instance)

        return instances

    def backup_instance(self, instance):
        """Create a backup (AMI) of a given instance"""
        image_id = self._connection.create_image(instance.id,
                                               self._create_AMI_name(instance))
        self._connection.create_tags([image_id],
                                     {'instance': instance.id,
                                      'created_at': datetime.date.today(),
                                      'created_by': 'cloudsnap'})
        return image_id

    def get_backups(self):
        """Return a list of all backups (AMIs) created by it"""
        backups = self._connection.get_all_images()

        return filter_backups_by_tags(backups, {"created_by": "cloudsnap"})

    def delete_backup(self, image):
        """Delete a backup (AMI)"""
        self._connection.deregister_image(image.id, True)
