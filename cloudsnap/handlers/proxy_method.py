from webapp2 import RequestHandler


class ProxyMethodRequestHandler(RequestHandler):
    """A Request Handler that enables the HTTP method to be overwrited by the
       querystring
    """
    def dispatch(self):
        """Overwrite RequestHandler's dispatch method to allow the HTTP method
           to be overwrited by the querystring parameter _method
        """
        if self.request.GET.get("_method"):
            self.request.method = self.request.GET.get("_method").upper()
        super(ProxyMethodRequestHandler, self).dispatch()
