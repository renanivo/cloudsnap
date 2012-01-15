from boto.ec2.connection import EC2Connection


def get_all_instances(connection):
    """Return a list of all instances of a EC2Connection"""
    instances = []

    for reservation in connection.get_all_instances():
        for instance in reservation.instances:
            instances.append(instance)

    return instances
