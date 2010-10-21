from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.labs import taskqueue
from models import Channel, ChannelEncoder 
from crawler import *
import logging

class TVFeed(webapp.RequestHandler):
    def get(self):
        json_encoder = ChannelEncoder(indent = 4)
        channels = list(Channel.all())
        self.response.out.write(json_encoder.encode(channels))

class RunCrawler(webapp.RequestHandler):
    def get(self):
        for ch in Channel.all():
            ch.delete()
        for c in CHANNELS_LIST:
            channel = Channel(img_url = c['img_url'], name = c['name'])
            channel.put()
            taskqueue.add(url = '/tvfeed/update', method = 'POST', 
                params = { 'key' : channel.key(), 'gogo_id' : c['c_id'] })
        self.response.out.write("Started")

    def post(self):
        key = self.request.get('key')
        gogo_id = self.request.get('gogo_id')
        updateInfo(key, gogo_id)

application = webapp.WSGIApplication(
    [('/tvfeed/json', TVFeed),('/tvfeed/update', RunCrawler)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
