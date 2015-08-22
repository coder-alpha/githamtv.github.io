from theplatform import *
import xml.etree.ElementTree as ET

try:
    from pyamf import remoting
    has_pyamf = True
except ImportError:
    has_pyamf = False

try:
    from sqlite3 import dbapi2 as sqlite

except:
    from pysqlite2 import dbapi2 as sqlite


class Nick(BaseChannel):
    short_name = 'nick'
    long_name = 'Nick Canada'
    base_url = 'http://www.nickcanada.com'
    default_action = 'root'

    def action_play_clip(self):
        urltemplate = 'http://ca.turbonick.nick.com/dynamo/turbonick/xml/dyn/media/mediaGen.jhtml?uri=mgid%3Atncms%3Avideo%3Anick.ca%3A'
        remote_url = urltemplate + self.args['clip_id']
        logging.debug('play_clip: %s' % remote_url)

        data = self.plugin.fetch(remote_url, max_age=self.cache_timeout)

        tree = ET.parse(data)
        root = tree.getroot()

        url = root.find('video/item/src').text
        logging.debug('remote_url: %s' % url)

        return self.plugin.set_stream_url(url)


    def action_get_episodes(self):
        url_template = 'http://www.nickcanada.com/Content/flash/xml/VideoData.ashx?showId=%s'
        url = url_template % self.args['id']

        data = self.plugin.fetch(url, max_age=self.cache_timeout)

        tree = ET.parse(data)
        root = tree.getroot()

        for info in root.findall('VideoInfo'):
            title = info.find('VideoTitle').text.replace('-', ' ')
            image = info.find('VideoThumbnail').text
            clipid = info.find('VideoLink').text

            # capitalize
            title = title[:1].upper() + title[1:]

            data = {}
            data.update(self.args)
            data.update({
                'Title': title,
                'action': 'play_clip',
                'clip_id': clipid,
                'Thumb': image
            })
            self.plugin.add_list_item(data, is_folder=False)
        self.plugin.end_list('episodes', [xbmcplugin.SORT_METHOD_DATE])

    def action_root(self):
        url = self.base_url + '/show'
        soup = BeautifulSoup(self.plugin.fetch(url, max_age=self.cache_timeout))

        allshows = soup.find('div', id='nick-shows-listings').findAll('a');
        shows = []

        for item in allshows:
            url = self.base_url + item['href']
            soup = BeautifulSoup(self.plugin.fetch(url, max_age=self.cache_timeout))

            valid = soup.find('li', id='nick-shows-watch-video');

            if (valid != None):


                data = {}
                data.update(self.args)
                data.update({
                    'Title': item.text.decode('unicode_escape'),
                    'action': 'get_episodes',
                    'remote_url': valid.a['href'],
                    'channel': self.short_name,
                    'id': item['href'].split('/')[3]
                })
                self.plugin.add_list_item(data)
        self.plugin.end_list('tvshows', [xbmcplugin.SORT_METHOD_LABEL])
