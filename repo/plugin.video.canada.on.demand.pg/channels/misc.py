import time
import cgi
import datetime
import simplejson
from channel import BaseChannel, ChannelException,ChannelMetaClass, STATUS_BAD, STATUS_GOOD, STATUS_UGLY
from utils import *
import httplib
import xbmcplugin
import xbmc
from channel import *

class CPAC(BaseChannel):
    short_name = 'cpac'
    long_name = "CPAC"
    default_action = 'root'
    base_url = "http://www.cpac.ca/forms/"
    icon_path = 'cpac.jpg'
    
    def action_play_video(self):
        remote_url = self.base_url + self.args['remote_url']
        soup = BeautifulSoup(self.plugin.fetch(remote_url, max_age=self.cache_timeout))
        obj = soup.find("object", {'id': "MPlayer2"})
        vidurl = obj.find('param', {'name': 'url'})['value']
        asx = BeautifulSoup(self.plugin.fetch(vidurl, max_age=self.cache_timeout))
        entries = asx.findAll('entry')
        if len(entries) > 1:
            entries = entries[1:]
        
        if len(entries) > 1:
            self.plugin.get_dialog().ok("Error", "Too Many Entries to play")
            return None
        
        url = entries[0].ref['href']
        return self.plugin.set_stream_url(url)
        
    def action_list_episodes(self):
        soup = BeautifulSoup(self.plugin.fetch(self.base_url + self.args['remote_url'], max_age=self.cache_timeout))
        for li in soup.find('div', {'id': 'video_scroll'}).findAll('div', {'class': 'list_item'}):
            links = li.findAll('a')
            ep_title = links[0].contents[0]
            show_title = links[1].contents[0]
            date_str = links[2].contents[0]
            self.plugin.add_list_item({
                'action': 'play_video',
                'channel': 'cpac',
                'remote_url': links[0]['href'],
                'Title': "%s (%s)" % (ep_title, date_str),
            }, is_folder=False)
            
            
        self.plugin.end_list()

    def action_list_shows(self):
        soup = BeautifulSoup(self.plugin.fetch(self.base_url, max_age=self.cache_timeout))
        select = soup.find('select', {"name": 'proglinks'})
        for show in select.findAll('option')[1:]:
            data = {}
            data.update(self.args)
            data['action'] = 'list_episodes'
            data['remote_url'] = show['value'].split("|",1)[1]
            data['Title'] = show.contents[0]
            self.plugin.add_list_item(data)
        self.plugin.end_list()
        
    def action_latest_videos(self):
        url = self.base_url + "index.asp?dsp=template&act=view3&section_id=860&template_id=860&hl=e"
        soup = BeautifulSoup(self.plugin.fetch(url, max_age=self.cache_timeout))
        for li in soup.find('div', {'id': 'video_scroll'}).findAll('div', {'class': 'list_item'}):
            links = li.findAll('a')
            ep_title = links[0].contents[0]
            show_title = links[1].contents[0]
            date_str = links[2].contents[0]
            logging.debug("VID: %s, %s" % (ep_title, show_title))
            self.plugin.add_list_item({
                'action': 'play_video',
                'channel': 'cpac',
                'remote_url': links[0]['href'],
                'Title': "%s - %s (%s)" % (show_title, ep_title, date_str),
            }, is_folder=False)
            
            
        self.plugin.end_list()
        
    def action_root(self):
        self.plugin.add_list_item({
            'action': 'latest_videos',
            'Title': 'Latest Videos',
            'channel': 'cpac',
        })
        self.plugin.add_list_item({
            'action': 'list_shows',
            'Title': 'All Shows',
            'channel': 'cpac',
        })
        self.plugin.end_list()
