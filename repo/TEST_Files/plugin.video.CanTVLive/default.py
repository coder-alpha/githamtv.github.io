import xbmcgui,xbmcplugin

plugin_handle = int(sys.argv[1])

_id = 'plugin.video.CanTVLive'
_icondir = "special://home/addons/" + _id + "/icons/"
fanart = "special://home/addons/" + _id + '/fanart.jpg'

def add_video_item(url, infolabels, img=''):
    listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, thumbnailImage=img)
    listitem.setInfo('video', infolabels)
    listitem.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, isFolder=False)
	
def add_item(url, infolabels, img=''):
    listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, thumbnailImage=img)
    listitem.setInfo('video', infolabels)
    listitem.setProperty('IsPlayable', 'False')
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, isFolder=True)


# Test

add_video_item('http://t2.llcdn.quickplay.com/live/hls/3505/s/livech3713/004.m3u8',{ 'title': 'INFO'}, '%s/links.png'% _icondir)
	
# Entertainment
add_video_item('http://link.theplatform.com/s/dtjsEC/77l1KA_G_5P1?feed=DEV%20Live%20Stream%20Feed',{ 'title': 'Global TV Halifax HD'}, '%s/GlobalHalifax.png'% _icondir)
add_video_item('http://link.theplatform.com/s/dtjsEC/EqBPGYLY6fEx?feed=DEV%20Live%20Stream%20Feed',{ 'title': 'Global TV Vancouver HD'}, '%s/GlobalBC.png'% _icondir)
add_video_item('http://link.theplatform.com/s/dtjsEC/hdSH3iztz_j_?feed=DEV%20Live%20Stream%20Feed',{ 'title': 'Global TV Toronto HD'}, '%s/GlobalToronto.png'% _icondir)
add_video_item('http://198.179.31.198/live/2059.high.stream/2059.high.stream/index.m3u8',{ 'title': 'CFCN CTV Lethbridge'}, '%s/CTV_Lethbridge.png'% _icondir)
add_video_item('http://198.179.31.198/live/2053.high.stream/2053.high.stream/index.m3u8',{ 'title': 'CFRN CTV Edmonton'}, '%s/CTV_Edmonton.png'% _icondir)
add_video_item('http://198.179.31.198/live/2062.high.stream/2062.high.stream/index.m3u8',{ 'title': 'CICC CTV Yorkton'}, '%s/CTV_Yorkton.png'% _icondir)
add_video_item('http://198.179.31.198/live/2056.high.stream/2056.high.stream/index.m3u8',{ 'title': 'CKCK CTV Regina'}, '%s/CTV_Regina.png'% _icondir)
add_video_item('rtmp://54.85.197.21:1935/live/news live=1 timeout=15',{ 'title': '[COLOR yellow]CHCH Hamilton HD[/COLOR]'}, '%s/CHCH_.png'% _icondir)
add_video_item('http://link.theplatform.com/s/dtjsEC/chjdYJxKb44V?manifest=m3u&feed=History%20Live%20Stream%20Feed',{ 'title': 'History (Canada) HD'}, '%s/history.png'% _icondir)
add_video_item('http://bcoveliveios-i.akamaihd.net/hls/live/207737/1942203455001/nat/master_Layer5.m3u8',{ 'title': 'Weather Network National HD'}, '%s/twn.png' % _icondir)
#DOWN add_video_item('http://bcoveliveios-i.akamaihd.net/hls/live/207737/1942203455001/atl/master.m3u8',{ 'title': 'Weather Network Atlantic HD'}, '%s/twn.png' % _icondir)
add_video_item('http://tscstreaming-lh.akamaihd.net/i/TSCLiveStreaming_1@91031/index_3_av-p.m3u8',{ 'title': 'The Shopping Channel HD'}, '%s/tsc.png'% _icondir)
add_video_item('http://tscstreaming-lh.akamaihd.net/i/TSCLiveStreaming_1@91031/index_3_av-b.m3u8',{ 'title': 'The Shopping Channel HD Alternate Link'}, '%s/tsc.png'% _icondir)
add_video_item('http://btflash-lh.akamaihd.net/i/BTTOFLASH_live@120219/master.m3u8',{ 'title': '[COLOR yellow]City TV Toronto HD[/COLOR]'}, '%s/CityTV.png'% _icondir)	
add_video_item('http://btflash-lh.akamaihd.net/i/BTMTLFLASH_live@120220/master.m3u8',{ 'title': '[COLOR yellow]City TV Montreal HD[/COLOR]'}, '%s/CityTV.png'% _icondir)	
add_video_item('http://btflash-lh.akamaihd.net/i/BTVANFLASH_live@120224/master.m3u8',{ 'title': '[COLOR yellow]City TV Vancouver HD[/COLOR]'}, '%s/CityTV.png'% _icondir)	
add_video_item('http://btflash-lh.akamaihd.net/i/BTCALFLASH_live@120221/master.m3u8',{ 'title': '[COLOR yellow]City TV Calgary HD[/COLOR]'}, '%s/CityTV.png'% _icondir)


# News
add_video_item('http://bcliveuniv-lh.akamaihd.net/i/cpac1eng2014_01@119330/index_2000_av-p.m3u8',{ 'title': 'CPAC HD'}, '%s/cpac-english.png'% _icondir)
add_video_item('http://bcliveuniv-lh.akamaihd.net/i/cpac1flr2014_01@51230/index_2000_av-p.m3u8',{ 'title': 'CPAC HD Alternate Link'}, '%s/cpac-english.png'% _icondir)
add_video_item('rtmp://a.cdn.newschat.tv/edge playpath=cbc_live swfUrl=http://msnbclive.eu/player.swf pageUrl=http://www.livenewschat.eu/canada/ live=1',{ 'title': 'CBC News'}, '%s/cbcnewsnetwork.png' % _icondir)
#DOWN add_video_item('http://ams-lp3.9c9media.com/hls-live/livepkgr/_definst_/liveeventNoDRM/cp24Open8.m3u8',{ 'title': 'CP24 News HD'}, '%s/CP24.png' % _icondir)
add_video_item('http://66.51.129.171:8080/demo/index.m3u8',{ 'title': 'CTV News HD'}, '%s/ctv_news.png' % _icondir)
add_video_item('http://ams-lp10.9c9media.com/hls-live/livepkgr/_definst_/liveNews/News18.m3u8',{ 'title': 'CTV News Live Feed 1 HD'}, '%s/CTVNews.png' % _icondir)
add_video_item('http://ams-lp7.9c9media.com/hls-live/livepkgr/_definst_/liveNews/News28.m3u8',{ 'title': 'CTV News Live Feed 2 HD'}, '%s/CTVNews.png' % _icondir)
add_video_item('http://ams-lp6.9c9media.com/hls-live/livepkgr/_definst_/liveNews/News38.m3u8',{ 'title': 'CTV News Live Feed 3 HD'}, '%s/CTVNews.png' % _icondir)
add_video_item('http://ams-lp5.9c9media.com/hls-live/livepkgr/_definst_/liveNews/News48.m3u8',{ 'title': 'CTV News Live Feed 4 HD'}, '%s/CTVNews.png' % _icondir)
add_video_item('http://hdflash_1-lh.akamaihd.net/i/cancbft_1@95875/index_1200_av-p.m3u8',{ 'title': 'CANCBFT (CBC French) HD'}, '%s/CBFT.png' % _icondir)
add_video_item('http://hdflash_1-lh.akamaihd.net/i/cancbft_1@95875/index_1200_av-b.m3u8',{ 'title': 'CANCBFT (CBC French) HD Alternate Link'}, '%s/CBFT.png' % _icondir)
add_video_item('rtmp://cp39414.live.edgefcs.net:443/live playpath=argent@9751 swfUrl=http://fpdownload.adobe.com/strobe/FlashMediaPlayback_101.swf/[[DYNAMIC]]/1 live=1 pageUrl=http://tele-en-direct.blogspot.com/2014/05/argent-tv-canada-en-direct.html',{ 'title': 'Argent (French)'}, '%s/argent.png' % _icondir)
add_video_item('rtmp://cp39414.live.edgefcs.net/live/ playpath=lcn2@9754 swfUrl=http://www.centraltv.fr/jwplayer/jwplayer.flash.swf live=1 pageUrl=http://www.centraltv.fr/canada-television/lcn-news',{ 'title': 'LCN News (French)'}, '%s/lcn.png' % _icondir)
add_video_item('http://frlive.artestras.cshls.lldns.net/artestras/contrib/frlive/frlive_925.m3u8',{ 'title': 'ARTE (French)'}, '%s/arte.png' % _icondir)


# Sports
add_video_item('http://s1.wssiptv.com/live/wssiptvdotcom/Mjhsn7sKhsC2e132/34.ts?12345678',{ 'title': 'TSN1 HD'}, '%s/tsn_1.png'% _icondir)
add_video_item('http://s1.wssiptv.com/live/wssiptvdotcom/Mjhsn7sKhsC2e132/35.ts?12345678',{ 'title': 'TSN2 HD'}, '%s/tsn_2.png'% _icondir)
add_video_item('http://s1.wssiptv.com/live/wssiptvdotcom/Mjhsn7sKhsC2e132/135.ts?12345678',{ 'title': 'TSN3 HD)'}, '%s/tsn_3.png'% _icondir)
add_video_item('http://s1.wssiptv.com/live/wssiptvdotcom/Mjhsn7sKhsC2e132/136.ts?12345678',{ 'title': 'TSN4 HD'}, '%s/tsn_4.png'% _icondir)
add_video_item('http://s1.wssiptv.com/live/wssiptvdotcom/Mjhsn7sKhsC2e132/137.ts?12345678',{ 'title': 'TSN5 HD'}, '%s/tsn_5.png'% _icondir)
add_video_item('http://nlds187.cdnak.neulion.com/nlds/sportsnetnow/sn_360/as/live/sn_360_hd_ipad.m3u8',{ 'title': 'Sportsnet 360 HD'}, '%s/sportsnet_360.png'% _icondir)
add_video_item('http://s1.wssiptv.com/live/wssiptvdotcom/Mjhsn7sKhsC2e132/76.ts?12345678',{ 'title': '[COLOR red]Sportsnet World HD[/COLOR]'}, '%s/sportsnet_world.png'% _icondir)
add_video_item('http://s1.wssiptv.com/live/wssiptvdotcom/Mjhsn7sKhsC2e132/75.ts?12345678',{ 'title': '[COLOR red]Sportsnet World One[/COLOR]'}, '%s/sportsnet_one.png'% _icondir)
add_video_item('http://s1.wssiptv.com/live/wssiptvdotcom/Mjhsn7sKhsC2e132/77.ts?12345678',{ 'title': '[COLOR red]Sportsnet World Ontario[/COLOR]'}, '%s/sportsnet_ontario.png'% _icondir)
#DOWN add_video_item('http://ams-lp9.9c9media.com/hls-live/livepkgr/_definst_/liveeventNoDRM/RDSOpen8.m3u8',{ 'title': 'RDS (French) HD'}, '%s/rds.png'% _icondir)
#DOWN add_video_item('http://ams-lp10.9c9media.com/hls-live/livepkgr/_definst_/liveeventNoDRM/RDS2Open8.m3u8',{ 'title': 'RDS2 (French) HD'}, '%s/rds2.png'% _icondir)
#DOWN add_video_item('http://ams-lp11.9c9media.com/hls-live/livepkgr/_definst_/liveeventNoDRM/RDSiOpen8.m3u8',{ 'title': 'RDS Info(French) HD'}, '%s/rds_info.png'% _icondir)
add_video_item('rtmp://cp39414.live.edgefcs.net/live/event1@9756',{ 'title': '[COLOR red]TVA Sports (French)[/COLOR]'}, '%s/TVA_Sports.png'% _icondir)

xbmcplugin.endOfDirectory(plugin_handle)
xbmc.executebuiltin("Container.SetViewMode(500)")

