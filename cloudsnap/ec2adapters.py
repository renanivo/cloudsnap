from boto.ec2.connection import EC2Connection
from boto.ec2.instance import Instance, Reservation

from settings import AWS


class EC2Account():

    _connection = None

    def __init__(self):
        self._connection = EC2Connection(AWS['key'],
                                         AWS['secret'],
                                         is_secure=AWS['use_safe_connection'])

    def get_instances(self):
        instances = []

        for reservation in self._connection.get_all_instances():
            for instance in reservation.instances:
                instances.append(instance)

        return instances
