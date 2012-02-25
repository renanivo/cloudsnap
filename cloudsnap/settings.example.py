AWS = {
    'key': '',
    'secret': '',
    'use_safe_connection': True
}

DEBUG = False

# From AppEngine documentation (http://goo.gl/AO8lt):
# For security purposes, the sender address of a message must be the email
# address of an administrator for the application or any valid email receiving
# address for the app (see Receiving Mail). The sender can also be the
# Google Account email address of the current user who is signed in, if the
# user's account is a Gmail account or is on a domain managed by Google Apps.
LOGGER = {
    'sender': 'Cloudsnap Logger<logger@appid.appspotmail.com>',
    'to': 'Your Email<you@yourdomain.com>',
}

# Template of the generated AMI's
# {{ today }} the current date in the format yyyy-mm-dd
# {{ name }} the instance name (falls back to instance_id when not found)
# {{ instance_id }}
AMI_NAME_TEMPLATE = "{{ today }}-{{ name }}"
