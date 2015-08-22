#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2012 Tristan Fischer (sphere@dersphere.de)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import plugintools
import xbmcgui,xbmcplugin
from xbmcswift2 import Plugin


STRINGS = {
    'Full Shows': 30103,
	'H101 Shows': 30101,
	

}

RSS_FEEDS = (
    {
        'title': 'Latest H101 Shows',
        'logo': 'H101.png',
        'stream_url': ('rss://db.tt/Q21JceYE'),
    },{
        'title': 'Latest H101 Shows (Alt)',
        'logo': 'H101.png',
        'stream_url': ('rss://kingofallmedia.s3.amazonaws.com/daily/daily.xml'),
    },
)


YOUTUBE_CHANNELS = (
    {
        'name': 'The Howard Stern Show',
        'logo': 'stern.png',
        'channel_id': 'UCSoKmLJ_lgYOJB-inayuTeA',
        'user': 'Howard Stern Full 2015',
    }, {
        'name': 'The Howard Stern Show (Alt)',
        'logo': 'stern.png',
        'channel_id': 'UC7eI5iCztDjL8A0RIaVyJcg',
        'user': 'Full Stern Shows',
    }, 
)



YOUTUBE_URL ='plugin://plugin.video.youtube/channel/%s/?page=1'

plugin = Plugin()


@plugin.route('/')
def show_root_menu():
    items = [
		 {'label': _('Latest Stern Shows'),
         'path': plugin.url_for('show_channels')},
         {'label': _('Latest H101 Shows'),
         'path': plugin.url_for('show_H101')},

    ]
    return plugin.finish(items)


@plugin.route('/streams/')
def show_streams():
    items = [{
        'label': stream['title'],
        'thumbnail': get_logo(stream['logo']),
        'path': stream['stream_url'],
        'is_playable': True,
    } for stream in STATIC_STREAMS]
    return plugin.finish(items)

	

@plugin.route('/H101/')
def show_H101():
    items = [{
        'label': stream['title'],
        'thumbnail': get_logo(stream['logo']),
        'path': stream['stream_url'],
        'is_playable': True,
    } for stream in RSS_FEEDS]
    return plugin.finish(items)

	

@plugin.route('/SternShow/')
def show_channels():
    items = [{
        'label': channel['name'],
        'thumbnail': get_logo(channel['logo']),
        'path': YOUTUBE_URL % channel['channel_id'],
    } for channel in YOUTUBE_CHANNELS]
    return plugin.finish(items)

def get_logo(logo):
    addon_id = plugin._addon.getAddonInfo('id')
    return 'special://home/addons/%s/resources/media/%s' % (addon_id, logo)


def _(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id])
    else:
        plugin.log.warning('String is missing: %s' % string_id)
        return string_id


def log(text):
    plugin.log.info(text)

if __name__ == '__main__':
    plugin.run()
