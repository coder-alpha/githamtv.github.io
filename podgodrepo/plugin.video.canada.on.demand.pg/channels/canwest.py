from theplatform import *
from BeautifulSoup import BeautifulStoneSoup
try:
    from pyamf import remoting
    has_pyamf = True
except ImportError:
    has_pyamf = False

class CanwestBaseChannel(ThePlatformBaseChannel):
    is_abstract = True
    base_url = 'http://feeds.theplatform.com/ps/JSON/PortalService/2.2/'
    PID = None
    root_depth = 1

    def get_categories_json(self,arg=None):
        return ThePlatformBaseChannel.get_categories_json(self) # + '&query=ParentIDs|%s'%arg

    def get_releases_json(self,arg='0'):
        return ThePlatformBaseChannel.get_releases_json(self) + '&query=CategoryIDs|%s'% (self.args['entry_id'],)

    def children_with_releases(self, categorylist, cat):

        if cat['fullTitle'] == '':
            prefix = ''
        else:
            prefix = cat['fullTitle'] + "/"

        children = [c for c in categorylist \
                    if c['depth'] == cat['depth'] + 1 \
                    and c['fullTitle'].startswith(prefix) \
                    and (c['hasReleases'] or self.children_with_releases(categorylist, c))]
        return children


    def get_child_categories(self, categorylist, parent_id):

        show_empty = self.plugin.get_setting('show_empty_cat') == 'true'
        if parent_id is None:
            if self.root_depth > 0:
                cat = [c for c in categorylist if c['depth'] == self.root_depth - 1][0]
            else:
                cat = {'depth': -1, 'fullTitle': ''}
        else:
            logging.debug("ParentID: %s [%s]" % (parent_id, type(parent_id)))
            cat = [c for c in categorylist if c['ID'] == int(parent_id)][0]

        if cat['fullTitle'] == '':
            prefix = ''
        else:
            prefix = cat['fullTitle'] + "/"

        if show_empty:
            categories = [c for c in categorylist if c['depth'] == cat['depth'] + 1 \
                          and c['fullTitle'].startswith(prefix)]

        else:
            categories = self.children_with_releases(categorylist, cat)

        return categories


    #override ThePlatFormbase so ?querystring isn't included in playpath
    #this could be temp-only, actually. paypath doesn't seem to care about extra parameters
    def action_play(self):
        parse = URLParser(swf_url=self.swf_url, playpath_qs=False)
        self.plugin.set_stream_url(parse(self.args['clip_url']))



class GlobalTV(CanwestBaseChannel):
    short_name = 'global'
    long_name = 'Global TV'
    PID = 'W_qa_mi18Zxv8T8yFwmc8FIOolo_tp_g'
    swf_url = 'http://www.globaltv.com/widgets/ThePlatformContentBrowser/swf/flvPlayer.swf swfvfy=true'
    #swf_url = 'http://www.globaltv.com/video/swf/flvPlayer.swf'

    def get_categories_json(self,arg=None):
        url = CanwestBaseChannel.get_categories_json(self,arg) + '&query=CustomText|PlayerTag|z/Global%20Video%20Centre' #urlencode
        logging.debug('get_categories_json: %s'%url)
        return url

    def get_releases_json(self,arg='0'):
        url = '%s' % CanwestBaseChannel.get_releases_json(self,arg)
        logging.debug('get_releases_json: %s'%url)
        return url

class GlobalNews(CanwestBaseChannel):
    base_url = 'http://globalnews.ca/national/videos'
    short_name = 'globalnews'
    long_name = 'Global News'
    local_channels = [
        ('National', 'http://globalnews.ca/national/videos'),
        ('BC', 'http://globalnews.ca/bc/videos'),
        ('Calgary', 'http://globalnews.ca/calgary/videos'),
        ('Halifax', 'http://globalnews.ca/halifax/videos'),
        ('Edmonton', 'http://globalnews.ca/edmonton/videos'),
        ('Lethbridge', 'http://globalnews.ca/lethbridge/videos'),
        ('Montreal', 'http://globalnews.ca/montreal/videos'),
        ('New Brunswick', 'http://globalnews.ca/new-brunswick/videos'),
        ('Okanagan', 'http://globalnews.ca/okanagan/videos'),
        ('Regina', 'http://globalnews.ca/regina/videos'),
        ('Saskatoon', 'http://globalnews.ca/saskatoon/videos'),
        ('Toronto', 'http://globalnews.ca/toronto/videos'),
        ('Winnipeg', 'http://globalnews.ca/winnipeg/videos'),
    ]

    def get_cache_key(self):
        return "%s-%s" % (self.short_name, self.args.get('local_channel',''))

    def action_root(self):
        for channel, ptag in self.local_channels:
            self.plugin.add_list_item({
                'Title': channel,
                'action': 'browse',
                'channel': self.short_name,
                'entry_id': None,
                'local_channel': channel
            })
        self.plugin.end_list()

    def action_browse(self):
        caturl = dict(self.local_channels)[self.args['local_channel']]

        #logging.debug('______________________________')
        #logging.debug('caturl: %s' % caturl)
        #logging.debug(self.args)
        #logging.debug(self.args['local_channel'])
        #logging.debug('______________________________')

        soup = BeautifulSoup(self.plugin.fetch(caturl, max_age=self.cache_timeout))
        navlist = soup.findAll('div', 'video-navigation-column')

        for index in range(len(navlist)):
            if (index == 0) and (self.args['local_channel'] == 'National'):
                continue

            catlinks = navlist[index].findAll('a')

            for category in catlinks:
                data = {}
                data.update(self.args)

                tagline = category.string
                url = category['href']

                data.update({
                    'action': 'browse_category',
                    'Title': tagline,
                    'entry_id': None,
                    'remote_url': url
                })
                self.plugin.add_list_item(data)
        self.plugin.end_list()

    def action_browse_category(self):
        logging.debug('______________________________')
        logging.debug(self.args)
        logging.debug('______________________________')

        # using RSS cuz json was not working
        # json.loads was complaining
        platform_url = 'http://feed.theplatform.com/f/dtjsEC/FCT_FJTDVpVT?form=rss&byId=%s'

        soup = BeautifulSoup(self.plugin.fetch(self.args['remote_url'], max_age=self.cache_timeout))
        eplist = soup.find('ul', 'video-browse-container').findAll('li')

        #logging.debug(eplist)

        for ep in eplist:
            spans = ep.findAll('span')
            duration = spans[len(spans)-1].string

            tagline = ep.a['title']

            # TODO: not sure why this is not loading...
            thumb = ep.img['src']
            if thumb:
                thumb = thumb.replace('&w=300', '')

            #logging.debug(thumb)

            data = {}
            data.update(self.args)

            data.update ({
                'action': 'play_episode',
                'entry_id': None,
            	'Title': tagline,
            	'Duration' : duration,
            	'Thumb' : thumb,
            	'tagline': tagline,
            	'remote_url': platform_url % ep.findAll('span')[1]['data-v_count_id']
            })
            self.plugin.add_list_item(data, is_folder=False)
        self.plugin.end_list()

    def action_play_episode(self):
        logging.debug('______________________________')
        logging.debug(self.args)
        logging.debug('______________________________')

        data = self.plugin.fetch(self.args['remote_url'], self.cache_timeout).read()
        soup = BeautifulStoneSoup(data)
        content = soup.find('media:content')

        url = content['url']
        logging.debug (url)

        return self.plugin.set_stream_url(url)



class HGTV(CanwestBaseChannel):
    short_name = 'hgtv'
    long_name = 'HGTV.ca'
    PID = 'HmHUZlCuIXO_ymAAPiwCpTCNZ3iIF1EG'
    #swf_url = 'http://www.hgtv.ca/includes/cwp/swf/flvPlayer.swf'

    def get_categories_json(self,arg):
        url = CanwestBaseChannel.get_categories_json(self,arg) + '&query=CustomText|PlayerTag|z/HGTVNEWVC%20-%20New%20Video%20Center' #urlencode
        logging.debug('get_categories_json: %s'%url)
        return url




    def add_releases(self):
        releases = self.get_releases(self.args)
        logging.debug("Got %s Releases: %s" % (len(releases), "\n".join(repr(r) for r in releases)))
        for rel in releases:
            self.plugin.add_list_item(rel, is_folder=False)


class SliceTV(CanwestBaseChannel):
    short_name = 'slice'
    long_name = 'Slice TV'
    PID = 'EJZUqE_dB8XeUUgiJBDE37WER48uEQCY'
    swf_url = 'http://www.slice.ca/includes/vc_20/swf/flvPlayer.swf'

    def get_categories_json(self,arg):
        url = CanwestBaseChannel.get_categories_json(self,arg) + '&query=CustomText|PlayerTag|z/SLICENEWVC%20-%20New%20Video%20Center' #urlencode
        logging.debug('get_categories_json: %s'%url)
        return url



class diyNet(CanwestBaseChannel):
    short_name = 'diynet'
    long_name = 'The DIY Network'
    PID = 'FgLJftQA35gBSx3kKPM46ZVvhP6JxTYt'
    #swf_url = 'http://www.diy.ca/Includes/cwp/swf/flvPlayer.swf'

    def get_categories_json(self,arg):
        url = CanwestBaseChannel.get_categories_json(self,arg) + '&query=CustomText|PlayerTag|z/DIY%20Network%20-%20Video%20Centre' #urlencode
        logging.debug('get_categories_json: %s'%url)
        return url



class ActionTV(CanwestBaseChannel):
    short_name = 'action'
    long_name = 'ActionTV'
    PID = 'gQ3jcVrUUZC_VoCqnqv_Tn_Q3BRUYIrl'

    def get_categories_json(self, arg=None):
        url = CanwestBaseChannel.get_categories_json(self) + '&query=CustomText|PlayerTag|z/Action%20Video%20Centre' #urlencode
        logging.debug('get_categories_json: %s'%url)
        return url