import datetime

from boto.ec2.connection import EC2Connection
from boto.ec2.instance import Instance, Reservation

from settings import AWS
from shortcuts import create_AMI_name


class EC2Account():

    _connection = None

    def __init__(self, connection=None):

        if connection is None:
            self._connection = EC2Connection(AWS['key'],
                                             AWS['secret'],
                                             is_secure=AWS['use_safe_connection'])
        else:
            self._connection = connection

    def get_instances(self):
        instances = []

        for reservation in self._connection.get_all_instances():
            for instance in reservation.instances:
                instances.append(instance)

        return instances

    def create_AMI(self, instance):
        image_id = self._connection.create_AMI(instance.id,
                                               create_AMI_name(instance))
        self._connection.create_tags([image_id],
                                     {'instance': instance.id,
                                      'created_at': datetime.date.today(),
                                      'created_by': 'cloudsnap'});
        return image_id
