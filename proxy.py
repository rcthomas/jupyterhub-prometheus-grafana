
import logging
import sys
from urllib.parse import quote

from jupyterhub.services.auth import HubAuthenticated
from jupyterhub.utils import url_path_join

from tornado import httpclient, httputil, ioloop, web

class ProxyHandler(HubAuthenticated, web.RequestHandler):
    hub_users = []
    allow_admin = True

    def initialize(self, proxy_url):
        self.proxy_url = proxy_url

    @web.authenticated
    async def get(self, proxied_path):
        return await self.proxy(proxied_path)

    @web.authenticated
    def post(self, proxied_path):
        return self.proxy(proxied_path)

    @web.authenticated
    def put(self, proxied_path):
        return self.proxy(proxied_path)

    @web.authenticated
    def delete(self, proxied_path):
        return self.proxy(proxied_path)

    @web.authenticated
    def head(self, proxied_path):
        return self.proxy(proxied_path)

    @web.authenticated
    def patch(self, proxied_path):
        return self.proxy(proxied_path)

    @web.authenticated
    def options(self, proxied_path):
        return self.proxy(proxied_path)

    async def proxy(self, proxied_path):

        if 'Proxy-Connection' in self.request.headers:
            del self.request.headers['Proxy-Connection']

        body = self.request.body
        if not body:
            if self.request.method == 'POST':
                body = b''
            else:
                body = None

        client = httpclient.AsyncHTTPClient()

        client_uri = url_path_join(self.proxy_url, proxied_path)
        if self.request.query:
            client_uri += '?' + self.request.query

        headers = self.proxy_request_headers()
        headers["X-WEBAUTH-USER"] = "admin"

        req = httpclient.HTTPRequest(
            client_uri, method=self.request.method, body=body,
            headers=headers, **self.proxy_request_options())

        try:
            response = await client.fetch(req, raise_error=False)
        except httpclient.HTTPError as err:
            # We need to capture the timeout error even with raise_error=False,
            # because it only affects the HTTPError raised when a non-200 response
            # code is used, instead of suppressing all errors.
            # Ref: https://www.tornadoweb.org/en/stable/httpclient.html#tornado.httpclient.AsyncHTTPClient.fetch
            if err.code == 599:
                self._record_activity()
                self.set_status(599)
                self.write(str(err))
                return
            else:
                raise

        # For all non http errors...
        if response.error and type(response.error) is not httpclient.HTTPError:
            self.set_status(500)
            self.write(str(response.error))
        else:
            self.set_status(response.code, response.reason)

            # clear tornado default header
            self._headers = httputil.HTTPHeaders()

            for header, v in response.headers.get_all():
                if header not in ('Content-Length', 'Transfer-Encoding',
                                  'Content-Encoding', 'Connection'):
                    # some header appear multiple times, eg 'Set-Cookie'
                    self.add_header(header, v)

            if response.body:
                self.write(response.body)

    def proxy_request_headers(self):
        '''A dictionary of headers to be used when constructing
        a tornado.httpclient.HTTPRequest instance for the proxy request.'''
        return self.request.headers.copy()

    def proxy_request_options(self):
        '''A dictionary of options to be used when constructing
        a tornado.httpclient.HTTPRequest instance for the proxy request.'''
        return dict(follow_redirects=False, connect_timeout=250.0, request_timeout=300.0)

def main(proxy_url):
    app = web.Application([
        (r"/services/grafana/(.*)", ProxyHandler, {"proxy_url": proxy_url})
    ])
    logging.critical('Dashboard listening on port %s.' % 8080)
    app.listen(8080)
    try:
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logging.critical('Shutting down...')

if __name__ == "__main__":
    main(sys.argv[1])
