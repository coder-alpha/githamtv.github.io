from brightcove import BrightcoveBaseChannel
from utils import *
from BeautifulSoup import BeautifulStoneSoup
import json
import logging
import xbmcplugin

class CorusBaseChannel(BrightcoveBaseChannel):

    is_abstract = True

    default_action = 'root'
    base_url = 'http://media.treehousetv.com'

    def action_root(self):
        # JSON data, but missing fields: url = "http://media.treehousetv.com/videos.ashx?c="
        soup = BeautifulSoup(self.plugin.fetch(self.base_url + "/", max_age=self.cache_timeout))

        player_id = None
        try:
            player_id = soup.find('object').find("param", {"name": "playerId"})['value']
        except:
            pass

        level0 = soup.find("ul", {"class": "level_0"})

        # Find all the categories but filter out the 'Full Episodes' group
        links = level0.findAll('a', {"class": "category-link", 'href':
            lambda a: "t=full+episodes" not in a})
        for link in links:
            data = {}
            data.update(self.args)
            data['Title'] = link.text
            data['action'] = 'list_episodes'
            data['query'] = link['href']
            data['player_id'] = player_id
            self.plugin.add_list_item(data)

        self.plugin.end_list()

    def action_list_episodes(self):
        query = self.args.get('query')

        data = self.plugin.fetch(self.base_url + "/videos.ashx" + query,
                max_age=self.cache_timeout).read()
        logging.debug(data)
        jdata = json.loads(data)

        for episode in jdata:
            data = {}
            data.update(self.args)
            data['Title'] = episode['Name']
            data['Plot'] = episode['ShortDescription']
            data['Thumb'] = episode['ThumbnailURL']
#            data['Duration'] = episode['Duration']

            data['action'] = 'play_video'
            data['showid'] = episode['Id']
            self.plugin.add_list_item(data, is_folder=False)
        self.plugin.end_list('episodes')

    def action_play_video(self):
        showid = self.args.get('showid')
        player_id = self.args.get('player_id')

        if not player_id:
            player_id = self.player_id

        info = self.get_clip_info(player_id, showid, self.publisher_id)
        self.video_id = showid
        self.get_swf_url()
        logging.debug(self.swf_url)
        parser = URLParser(swf_url=self.swf_url, swf_verify=True)
        url = self.choose_rendition(info['renditions'])['defaultURL']

        app, playpath = url.split("&")
        qs = "?videoId=%s&lineUpId=&pubId=%s&playerId=%s&affiliateId=" % (self.video_id, self.publisher_id, player_id)
        scheme,netloc = app.split("://")

        netloc, app = netloc.split("/",1)
        app = app.rstrip("/") + qs
        logging.debug("APP:%s" %(app,))
        tcurl = "%s://%s:1935/%s" % (scheme, netloc, app)
        logging.debug("TCURL:%s" % (tcurl,))
        url = "%s app=%s playpath=%s swfUrl=%s swfVfy=true pageUrl=%s" %(tcurl, app, playpath,
                self.swf_url, "http://media.treehousetv.com")
        self.plugin.set_stream_url(url)

class TreehouseTV(CorusBaseChannel):
    short_name = 'treehouse'
    long_name = 'Treehouse TV'

    base_url = 'http://media.treehousetv.com'

    # dynamically load this, default id:
    player_id = 904944191001

    publisher_id = 694915333001
    flash_experience_id="myExperience"

class YTV(CorusBaseChannel):
    short_name = 'ytv'
    long_name = 'YTV'

    base_url = "http://www.ytv.com/videos"

    # dynamically load this, default id:
    player_id = 904863021001

    publisher_id = 694915334001
    flash_experience_id="myExperience"

    token= '1372009211_46a528e32299a06a17b91387b1c9cf48'
    swf_url = 'http://pdk.theplatform.com/pdk/swf/flvPlayer.swf'


    # ytv player
    # http://player.theplatform.com/p/yT_qKC/Main-Player

    feed_url = "http://feed.theplatform.com/f/yT_qKC/tvQ0Oy74AVLa/"
    show_params = "Victorious%7CShows+N-Z%2FSplatalot%7CShows+A-F%2FBig+Time+Rush%7CShows+N-Z%2FSidekick%7CMr.+Young%7CShows+N-Z%2FPower+Rangers+Megaforce%7CShows+N-Z%2FTUFF+Puppy%7CShows+G-M%2FLeague+Of+Super+Evil%7CShows+A-F%2FBeyblade%7CShows+N-Z%2FZoink%27d%7CTotally+Amp%27d%7CLife+With+Boys%7CFeatured%7CCrunch%7CSpongeBob+SquarePants%7CThe+Zone%7CShows+G-M%2FMarvin+Marvin%7CShows+N-Z%2FThat%27s+So+Weird%7CExtreme+Babysitting%7CShows+N-Z%2FThe+Next+Star%7CFull+Episodes%7CShows+N-Z%2FRated+A+For+Awesome%7CShows+A-F%2FAlmost+Naked+Animals%7CiCarly%7CShows+G-M%2FHow+to+Rock%7CShows+N-Z%2FScaredy+Squirrel%7CShows+A-F%2FCache+Craze%7CShows+A-F%2FFairly+OddParents%7CShows+N-Z%2FTeenage+Mutant+Ninja+Turtles%7CMusic+Videos%7CBig+Fun+Movies"
    cat_start_params = "categories/?byFullTitle="
    cat_end_params = "&types=none&fields=fullTitle,id,label,order,parentId,title&validFeed=false&form=rss"
    rel_start_params = "?range=1-100&byCategories="
    rel_end_params = "&validFeed=false&count=true&fields=author,content,defaultThumbnailUrl,description,pubDate,title&types=none&byContent=byFormat=mpeg4|f4m|flv&fileFields=bitrate,duration,format,url&params=player=YTV%20-%20Video%20Page%20Player&form=rss"

    def action_root(self):
        url = self.feed_url + self.cat_start_params + self.show_params + self.cat_end_params
        soup = BeautifulStoneSoup(self.plugin.fetch(url, max_age=self.cache_timeout)
                        , convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        shows = soup.findAll('item')

        for show in shows:
            show_title = show.title.string

            try:
                show_fullTitle = show.find('plcategory:fulltitle').string

                # there are categories, so add to the list
                self.plugin.add_list_item({
                    'Title': show_title,
                    'action': 'list_episodes',
                    'channel': self.short_name,
                    'fulltitle': show_fullTitle
                })
            except: pass
        self.plugin.end_list('tvshows', [xbmcplugin.SORT_METHOD_LABEL])

    def action_list_episodes(self):
        url = self.feed_url + self.rel_start_params + self.show_params + ',' + self.args['fulltitle'] + self.rel_end_params
        #logging.debug('______________________________')
        #logging.debug(url)
        #logging.debug('______________________________')

        soup = BeautifulStoneSoup(self.plugin.fetch(url, max_age=self.cache_timeout)
                        , convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        episodes = soup.findAll('item')

        for episode in episodes:
            ep_title = episode.title.string
            ep_plot = episode.description.string

            ep_media = episode.find('media:content')
            ep_duration = int(float(ep_media['duration']) / 60)
            ep_url = ep_media['url']

            #ep_thumb = episode.find('plmedia:defaultThumbnailUrl')

            data = {}
            data.update(self.args)

            data.update ({
                'action': 'play_episode',
                'entry_id': None,
            	'Title': ep_title,
            	'Duration' : ep_duration,
            	'Plot': ep_plot,
            	#'Thumb' : ep_thumb,
            	'tagline': ep_title,
            	'remote_url': ep_url
            })
            self.plugin.add_list_item(data, is_folder=False)
        self.plugin.end_list('episodes', [xbmcplugin.SORT_METHOD_DATE])

    def action_play_episode(self):
        url = self.args['remote_url']
        logging.debug('______________________________')
        logging.debug(url)
        logging.debug('______________________________')
        return self.plugin.set_stream_url(url)
