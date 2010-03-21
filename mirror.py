from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch, memcache
import logging

class MainPage(webapp.RequestHandler):
    def get_feed(self):
        data = memcache.get('data')
        if data is not None:
            logging.debug('feed was cached')
            return data
        else:
            data = urlfetch.fetch('http://www.rfs.nsw.gov.au/feeds/majorIncidents.xml')
            # Obviously ignoring the "Cache-Control: no-cache" header returned here
            # And caching for sixty seconds
            memcache.add('data', data, 60)
            logging.debug('feed was NOT CACHED - got a new copy')
            return data
        
    def get(self):
        data = self.get_feed()

        # TODO: Should probably override the Content-Location header
        # TODO: Set the "Age" header
        for key, value in data.headers.iteritems():
            self.response.headers[key] = value
        self.response.out.write(data.content)

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
