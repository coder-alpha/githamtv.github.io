import time
import cgi
import datetime
import simplejson
from channel import BaseChannel, ChannelException,ChannelMetaClass, STATUS_BAD, STATUS_GOOD, STATUS_UGLY
from utils import *
import httplib
import xbmcplugin
import xbmc

try:
    from pyamf import remoting
    has_pyamf = True
except ImportError:
    has_pyamf = False
    

    
class BrightcoveBaseChannel(BaseChannel):
    
    is_abstract = True
    

    def get_swf_url(self):
        conn = httplib.HTTPConnection('c.brightcove.com')
        qsdata = dict(width=640, height=480, flashID=self.flash_experience_id, 
                      bgcolor="#000000", playerID=self.player_id, publisherID=self.publisher_id,
                      isSlim='true', wmode='opaque', optimizedContentLoad='true', autoStart='', debuggerID='')
        qsdata['@videoPlayer'] = self.video_id
        logging.debug("SWFURL: %s" % (urllib.urlencode(qsdata),))
        conn.request("GET", "/services/viewer/federated_f9?&" + urllib.urlencode(qsdata))
        resp = conn.getresponse()
        location = resp.getheader('location')
        base = location.split("?",1)[0]
        location = base.replace("BrightcoveBootloader.swf", "connection/ExternalConnection_2.swf")
        self.swf_url = location
        
    def get_clip_info(self, player_id, video_id, publisher_id):
        conn = httplib.HTTPConnection("c.brightcove.com")
        envelope = self.build_amf_request(player_id, video_id, publisher_id)
        conn.request("POST", "/services/messagebroker/amf?playerid=" +
                str(player_id), str(remoting.encode(envelope).read()), {'content-type': 'application/x-amf'})
        response = conn.getresponse().read()
        response = remoting.decode(response).bodies[0][1].body
        logging.debug(response)
        return response
   
    def choose_rendition(self, renditions):
        maxrate = int(self.plugin.get_setting("max_bitrate")) * 1024
        rends = [r for r in renditions if r['encodingRate'] < maxrate]
        if not rends:
            rends = renditions
        rends.sort(key=lambda r: r['encodingRate'])
        return rends[-1]
    
    def build_amf_request_body(self, player_id, video_id, publisher_id):
        # const b956f752886e0e38a5ad4ffef43f48c839316602, class id?
        return [
                u'b956f752886e0e38a5ad4ffef43f48c839316602',
                player_id,
                video_id,
                publisher_id,
                ]


    def build_amf_request(self, player_id, video_id, publisher_id):
        env = remoting.Envelope(amfVersion=3)
        env.bodies.append(
            (
                "/1",
                remoting.Request(
                    target="com.brightcove.player.runtime.PlayerMediaFacade.findMediaById",
                    body=self.build_amf_request_body(player_id, video_id,
                        publisher_id),
                    envelope=env
                )
            )
        )
        return env


    def find_ids(self, url):
        soup = BeautifulSoup(self.plugin.fetch(url, max_age=self.cache_timeout))
        self.flash_experience_id = soup.find("object")['id']
        try:
            player_id = int(soup.find("object").find("param", {"name": "playerID"})['value'])
        except:
            player_id = None
            
        try:
            video_id = int(soup.find('object').find("param", {"name": "@videoPlayer"})['value'])
        except:
            video_id = None
        
        return player_id, video_id

class TVOKids(BrightcoveBaseChannel):
    
    short_name = 'tvokids'
    long_name = 'TVO Kids'
    default_action = 'root'
    base_url  = 'http://www.tvokids.com'
    player_id = 48543011001
    publisher_id = 15364602001
    flash_experience_id="null"

    def get_swf_url(self):
        conn = httplib.HTTPConnection('c.brightcove.com')
        qsdata = dict(width=640, height=480, flashID=self.flash_experience_id, 
                      bgcolor="#000000", playerID=self.player_id, publisherID=self.publisher_id,
                      isSlim='true', wmode='opaque', optimizedContentLoad='true', autoStart='', debuggerID='')
        qsdata['@videoPlayer'] = self.video_id
        logging.debug("SWFURL: %s" % (urllib.urlencode(qsdata),))
        conn.request("GET", "/services/viewer/federated_f9?&" + urllib.urlencode(qsdata))
        resp = conn.getresponse()
        location = resp.getheader('location')
        base = location.split("?",1)[0]
        location = base.replace("BrightcoveBootloader.swf", "federatedVideo/BrightcovePlayer.swf")
        self.swf_url = location
            
    def action_root(self):
        data = {}
        data.update(self.args)
        data['action'] = 'list_shows'
        data['age'] = 5
        data['Title'] = "Ages 2-5"
        self.plugin.add_list_item(data)
        data['Title'] = "Ages 11 and under"
        data['age'] = 11
        self.plugin.add_list_item(data)
        self.plugin.end_list()
            
    def action_play_video(self):
        info = self.get_clip_info(self.player_id, self.args['bc_id'],
                self.publisher_id)
        self.video_id = self.args.get('bc_id')
        self.get_swf_url()
        logging.debug(self.swf_url)
        parser = URLParser(swf_url=self.swf_url, swf_verify=True)
        url = self.choose_rendition(info['renditions'])['defaultURL']
        app, playpath, wierdqs = url.split("&", 2)
        qs = "?videoId=%s&lineUpId=&pubId=%s&playerId=%s&affiliateId=" % (self.video_id, self.publisher_id, self.player_id)
        #playpath += "&" + wierdqs
        scheme,netloc = app.split("://")
        
        netloc, app = netloc.split("/",1)
        app = app.rstrip("/") + qs
        logging.debug("APP:%s" %(app,))
        tcurl = "%s://%s:1935/%s" % (scheme, netloc, app)
        logging.debug("TCURL:%s" % (tcurl,))
        #pageurl = 'http://www.tvokids.com/shows/worldofwonders'
        url = "%s tcUrl=%s app=%s playpath=%s%s swfUrl=%s conn=B:0 conn=S:%s&%s" % (tcurl,tcurl, app, playpath, qs, self.swf_url, playpath, wierdqs)
        logging.debug(url)
        self.plugin.set_stream_url(url)
        
        
    def action_browse_show(self):
        url = self.base_url + "/feeds/%s/all/videos_list.xml?random=%s" % (self.args['node_id'], int(time.time()), )
        page = self.plugin.fetch(url, max_age=self.cache_timeout).read()
        soup = BeautifulStoneSoup(page)
        for node in soup.findAll('node'):
            data = {}
            logging.debug(node)
            data.update(self.args)
            data['action'] = 'play_video'
            data['Thumb'] = node.find('node_still').contents[0].strip()
            data['Title'] = decode_htmlentities(node.find('node_title').contents[0].strip())
            data['Plot'] = decode_htmlentities(node.find("node_short_description").contents[0].strip())
            data['bc_id'] = node.find("node_bc_id").contents[0].strip()
            data['bc_refid'] = node.find("node_bc_refid").contents[0].strip()
            self.plugin.add_list_item(data, is_folder=False)
        self.plugin.end_list('episodes')
        
    def action_list_shows(self):
        age = int(self.args.get('age'))
        if age == 11:
            url = '/feeds/all/98/shows'
        elif age == 5:
            url = '/feeds/all/97/shows'
        page = self.plugin.fetch(self.base_url + url, max_age=self.cache_timeout).read()
        soup = BeautifulStoneSoup(page)
        for node in soup.findAll('node'):
            data = {}
            data.update(self.args)
            data['Title'] = decode_htmlentities(node.find('node_title').contents[0].strip())
            thumb = node.find('node_thumbnail').contents[0].strip()
            if not thumb.endswith(".swf"):
                data['Thumb'] = self.base_url + "/" + thumb
            data['node_id'] = node.find('node_id').contents[0].strip()
            data['action'] = 'browse_show'
            self.plugin.add_list_item(data)
        self.plugin.end_list()
        