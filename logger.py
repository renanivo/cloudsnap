import datetime

import webapp2
from google.appengine.api import mail

from settings import LOGGER

class Logger:

    @staticmethod
    def log(handler, message):
        if not isinstance(handler, webapp2.RequestHandler):
            raise LoggerError("parameter given is not a webapp2 RequestHandler")

        subject = ("Cloudsnap Log at %s" % datetime.date.today())

        handler.response.out.write(message)
        mail.send_mail(sender=LOGGER['sender'], to=LOGGER['to'],
                       subject=subject, body=message)


class LoggerError(Exception):
    """Logger Exception class for Cloudsnap"""
    pass
