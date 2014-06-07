# coding=utf-8
import logging
import time
import functools
import datetime


class LogFunctionDecorator(object):
    """decorate a function to log its execution"""

    def __init__(self, func):
        self.func = func
        self.elapsed_time = 0

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        result = self.func(*args, **kwargs)
        self.elapsed_time = time.time() - start_time

        message = u"""
        %(now)s: %(name)s executed in %(elapsed).6f secs with %(params)s
        """

        logging.info(message % self._get_log_data(args, kwargs))
        return result

    def _get_log_data(self, params, kw_params):
        return {u"name": self.func.__name__,
                u"elapsed": self.elapsed_time,
                u"now": datetime.datetime.now(),
                u"params": "args: %s and kwargs: %s" % (params, kw_params)}


class LogMethodDecorator(LogFunctionDecorator):
    """decorate a method to log its execution"""
    def __init__(self, func):
        super(LogMethodDecorator, self).__init__(func)

    def _get_log_data(self, params, kw_params):
        try:
            class_name = params[0].__class__.__name__
        except AttributeError:
            class_name = params[0].__name__

        data = super(LogMethodDecorator, self)._get_log_data(params, kw_params)
        data[u"name"] = "%s.%s" % (class_name, self.func.__name__)

        return data


def log_function(func):
    """
    decorate a function to log its execution keeping its __name__ and __doc__
    """
    decorated = LogFunctionDecorator(func)

    @functools.wraps(func)
    def helper(*args, **kwargs):
        return decorated(*args, **kwargs)

    return helper


def log_method(func):
    """
    decorate a method to log its execution keeping its __name__ and __doc__
    """
    decorated = LogMethodDecorator(func)

    @functools.wraps(func)
    def helper(*args, **kwargs):
        return decorated(*args, **kwargs)

    return helper
