import datetime

import jinja2

from boto.ec2.connection import EC2Connection
from boto.ec2.instance import Instance, Reservation

from settings import AWS, AMI_NAME_TEMPLATE


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
        instances = []

        for reservation in self._connection.get_all_instances():
            for instance in reservation.instances:
                instances.append(instance)

        return instances

    def backup_instance(self, instance):
        image_id = self._connection.create_image(instance.id,
                                               self._create_AMI_name(instance))
        self._connection.create_tags([image_id],
                                     {'instance': instance.id,
                                      'created_at': datetime.date.today(),
                                      'created_by': 'cloudsnap'});
        return image_id


    def get_backups(self):
        return self._connection.get_all_images()
