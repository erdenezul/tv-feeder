# -*- coding: utf-8 -*-
from google.appengine.ext import db
import re
import logging
from urllib import urlopen
from models import Channel,Program

CHANNELS_LIST = [
   {'img_url': 'http://stat.gogo.mn/images/tv/small_mn.gif','name':u'МҮОНРТ','c_id':1},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_ubs.gif','name':u'UBS','c_id':2},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_tv25.gif','name':u'MN25','c_id':3},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_tv5.gif', 'name':'TV5','c_id':4},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_tv9.gif', 'name':'TV9','c_id':8},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_c1.gif', 'name':'C1','c_id':9},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_ntv.gif','name':'NTV','c_id':10},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_tv8.gif', 'name':'TV8','c_id':11},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_nbs.gif', 'name':'NBS', 'c_id':'15'},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_tm.gif', 'name':u'TM','c_id':12},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_sbn.gif', 'name':'SBN','c_id':13},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_bolovsrol.gif','name':u'БОЛОВСРОЛ','c_id':14},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_eagletv.gif','name':'EagleTV','c_id':17},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_btv.gif','name':'BTV','c_id':16},
   {'img_url': 'http://stat.gogo.mn/images/tv/small_sch.gif', 'name':u'МОНГОЛ TV','c_id':18},
]
URL = "http://news.gogo.mn/tvguide/content/tv.jsp?tvId=%s&typeId=pro_all&week=%s"


def updateInfo(key, gogo_id):
    channel = Channel.get(key)
    programs = list(Program.gql("WHERE channel = :channel", channel = channel))
    for p in programs:
        p.delete()
    for day in range(1,8): #iterate week
        logging.info('updating info of ' + channel.name)
        try:
            updatePrograms(channel, day, gogo_id)
        except Exception, e:
            logging.error('error happened, while updating: ' + e.message)

def updatePrograms(channel, week_id, c_id):
    maked_url = URL % (c_id, week_id)
    response = urlopen(maked_url)
    html = response.read()
    response.close()
    filtered_list = re.findall(r'<td.*?><span.*?>(.*?)</span></td>',html)
    for i in range(0,len(filtered_list),2):
        time = filtered_list[i]
        name = filtered_list[i+1].decode('utf-8')
        p = Program( day=week_id, time = time, name = name, channel = channel)
        p.put()
