from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.labs import taskqueue
from models import Channel, ChannelEncoder 
from crawler import *
import logging

is_modified = True
cached_response = ""

class TVFeed(webapp.RequestHandler):
    def get(self):
        global is_modified, cached_response
        if is_modified:
            response = ""
            for c in Channel.all():
                response += c.name + '#' + c.img_url + '\n'
                for i in range(1,8):
                    programs = Program.gql("WHERE day = :day AND channel = :channel", day = i, channel = c)
                    response += '\t' + str(i) + '\n'
                    for p in programs:
                        response += '\t\t' + p.time + '#' + p.name + '\n'
            cached_response = response
            is_modified = False
            logging.info('cached response')
            self.response.out.write(response)
        else:
            logging.info('responding from cache')
            self.response.out.write(cached_response)

class RunCrawler(webapp.RequestHandler):
    def get(self):
        global is_modified
        is_modified = True
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
    [('/tvfeed/json', TVFeed),('/tvfeed/update', RunCrawler),],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
