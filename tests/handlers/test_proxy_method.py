import unittest
from mock import patch

from handlers import ProxyMethodRequestHandler
import webapp2


class StubHandler(ProxyMethodRequestHandler):

    def post(self):
        pass

    def put(self):
        pass

class ProxyMethodRequestHandlerTest(unittest.TestCase):

    @patch.object(StubHandler, "post")
    def test_should_rewrite_the_request_method_using_querystring(self,
                                                                 mock_post):
        request = webapp2.Request.blank("/?_method=post")
        request.route = webapp2.Route("/", StubHandler)
        request.route_args = tuple()
        request.route_kwargs = {}

        handler = StubHandler(request)
        handler.dispatch()

        mock_post.assert_called_once()

    @patch.object(StubHandler, "put")
    def test_should_not_rewrite_the_request_method_without_querystring(self,
                                                                    mock_put):
        request = webapp2.Request.blank("/")
        request.method = "PUT"
        request.route = webapp2.Route("/", StubHandler)
        request.route_args = tuple()
        request.route_kwargs = {}

        handler = StubHandler(request)
        handler.dispatch()

        mock_put.assert_called_once()
