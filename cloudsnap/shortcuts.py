import datetime

import jinja2
from boto.ec2.connection import EC2Connection


def get_all_instances(connection):
    """Return a list of all instances of a EC2Connection"""
    instances = []

    for reservation in connection.get_all_instances():
        for instance in reservation.instances:
            instances.append(instance)

    return instances

def create_instance_backup_name(template, instance):
    env = jinja2.Environment()
    template = env.from_string(template)

    name = instance.tags["Name"] if instance.tags.has_key("Name") else instance.id

    return template.render({
        "today": datetime.date.today(),
        "name": name,
        "instance_id": instance.id,
        })
