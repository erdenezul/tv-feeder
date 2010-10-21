from google.appengine.ext import db
try: 
    import json
except ImportError:
    import simplejson as json
import datetime
import logging

class Channel(db.Model):
    img_url = db.TextProperty()
    name = db.StringProperty()

class Program(db.Model):
    day = db.IntegerProperty()
    time = db.StringProperty()
    name = db.TextProperty()
    channel = db.ReferenceProperty(Channel)

class ChannelEncoder(json.JSONEncoder):
    def default(self, obj):
        if(isinstance(obj, Channel)):
            logging.info('encoding ' + obj.name)
            programs = list(Program.all().filter('channel = ', obj))
            program_list = []
            for p in programs:
                program_list.append({ 'day' : p.day, 'time' : p.time, 'program_name' : p.name })
            return { "img_url" : obj.img_url, "name": obj.name, 'programs' : program_list }
        return json.JSONEncoder.default(self, obj)
            
        
