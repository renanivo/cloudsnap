import datetime

import jinja2
from boto.ec2.connection import EC2Connection


def create_instance_backup_name(template, instance):
    env = jinja2.Environment()
    template = env.from_string(template)

    name = instance.tags["Name"] if instance.tags.has_key("Name") else instance.id

    return template.render({
        "today": datetime.date.today(),
        "name": name,
        "instance_id": instance.id,
        })
