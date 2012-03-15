import datetime

import jinja2
from boto.ec2.connection import EC2Connection

from settings import AMI_NAME_TEMPLATE


def create_AMI_name(instance):
    env = jinja2.Environment()
    template = env.from_string(AMI_NAME_TEMPLATE)

    name = instance.tags["Name"] if instance.tags.has_key("Name") else instance.id

    return template.render({
        "today": datetime.date.today(),
        "name": name,
        "instance_id": instance.id,
        })
