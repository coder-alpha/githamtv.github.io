import fnmatch, os, sys, urllib
from os.path import join, getsize
from urllib2 import quote
from datetime import datetime

DROPBOX_ID = '7800535'
BASE_URL = 'http://podgod.webege.com/Repo/My-Repo/TEST Files/M3U/' % (DROPBOX_ID)
PODCAST_TITLE = 'Latest M3U Lists'
DESCRIPTION = 'For private use only. I take no responsibility in what you download. Enjoy!'

feed_template = """<?xml version="1.0" encoding="ISO-8859-1"?>
  <rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
    <channel>
      <description>%s</description>
      <link>%s/feed.xml</link>
      <title>%s</title>
      <pubDate>%s</pubDate>
        <!--data-feed -->
    </channel>
  </rss>
  """ % (DESCRIPTION, BASE_URL, PODCAST_TITLE, datetime.now())

def main():

  feed = ''
  for dirname, dirnames, files in os.walk('.'):
    dirname_enc = urllib.quote(dirname[2:].replace(u'\\', u'/'))
    for filename in files:
      if not fnmatch.fnmatch(filename, '*.m3u'):
        continue
      mp3_url = quote(filename)
      title = filename.replace('&','&amp;')
      size = getsize(join(dirname, filename))

      link = '%s%s/%s' % (BASE_URL, dirname_enc, mp3_url)
      feed += """<item>
                  <title>%s</title>
                  <link>%s</link>
                  <enclosure type="audio/mpeg" length="%s" url="%s"/>
                  </item>""" % (title, link, size, link)  

  feed_data = feed_template.replace('<!--data-feed -->',feed)
  f = open("feed.xml", 'w')
  f.write(feed_data)
  f.close()

if __name__ == '__main__':
  main()