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
	'Latest IPTV Links': 30101,
}

IPTV_LINKS = (
    {
        'title': '[B][COLOR red]U[COLOR][COLOR white]S[COLOR][COLOR darkblue]A[/COLOR][COLOR red] T[/COLOR][COLOR white]V[/COLOR][/B]',
        'logo': 'us.png',
        'stream_url': ('http://podgod.webege.com/Repo/My-Repo/TEST_Files/M3U/M3U/usa.m3u'),
    },{
        'title': '[B][COLOR red]U[/COLOR][COLOR darkblue]K[/COLOR][COLOR red] T[/COLOR][COLOR darkblue]V[/COLOR][/B]',
        'logo': 'uk.png',
        'stream_url': ('http://podgod.webege.com/Repo/My-Repo/TEST_Files/M3U/M3U/uk.m3u'),
    },{
        'title': '[B][COLOR red]C[/COLOR][COLOR white]A[/COLOR][COLOR red]N[/COLOR][COLOR white]A[/COLOR][COLOR red]D[/COLOR][COLOR white]A[/COLOR][COLOR red] T[/COLOR][COLOR white]V[/COLOR][/B]',
        'logo': 'canada.png',
        'stream_url': ('http://podgod.webege.com/Repo/My-Repo/TEST_Files/M3U/M3U/Canada.xml'),
    },{
        'title': '[B][COLOR blue]S[/COLOR][COLOR red]p[/COLOR][COLOR green]o[/COLOR][COLOR yellow]r[/COLOR][COLOR orange]t[/COLOR][COLOR brown]s[/COLOR][/B] Channels',
        'logo': 'sports.png',
        'stream_url': ('http://podgod.webege.com/Repo/My-Repo/TEST_Files/M3U/M3U/sports.m3u'),
    },{
        'title': '[B][COLOR light blue]WSS - [COLOR blue]SKY[/COLOR] Cable[/COLOR][/B] Channels',
        'logo': 'sky.png',
        'stream_url': ('http://podgod.webege.com/Repo/My-Repo/TEST_Files/M3U/M3U/WSSSky.m3u'),
    },{
        'title': '[B][COLOR purple]3RD Party Lists[/COLOR][/B]',
        'logo': 'test.png',
        'stream_url': ('http://podgod.webege.com/Repo/My-Repo/TEST_Files/M3U/M3U/PGTV1.m3u'),
    },
)

plugin = Plugin()

@plugin.route('/')
def show_root_menu():
    items = [
		 {'label': _('[B][COLOR blue]***Latest IPTV Links***[/COLOR][/B]'),
         'path': plugin.url_for('show_IPTV')},

    ]
    return plugin.finish(items)


@plugin.route('/IPTV/')
def show_IPTV():
    items = [{
        'label': stream['title'],
        'thumbnail': get_logo(stream['logo']),
        'path': stream['stream_url'],
        'is_playable': True,
    } for stream in IPTV_LINKS]
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
