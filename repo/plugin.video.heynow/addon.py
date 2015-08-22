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


RSS_FEEDS = (
    {
        'title': 'Main Shows',
        'logo': 'stern.png',
        'stream_url': ('rss://kingofallmedia.s3.amazonaws.com/daily/daily.xml'),
    },
)


plugin = Plugin()


@plugin.route('/')
def show_root_menu():
    items = [{
        'label': stream['title'],
        'thumbnail': get_logo(stream['logo']),
        'path': stream['stream_url'],
        'is_playable': True,
    } for stream in RSS_FEEDS]
    return plugin.finish(items)

	
def get_logo(logo):
    addon_id = plugin._addon.getAddonInfo('id')
    return 'special://home/addons/%s/resources/media/%s' % (addon_id, logo)

if __name__ == '__main__':
    plugin.run()
