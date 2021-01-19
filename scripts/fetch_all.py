import os
import sys

import django
import dateutil.parser as dparser
import feedparser

sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'merofeed.settings')
django.setup()

from feed.models import Site, Topic, Post, Subscription

def fetch_site_urls_by_topic(topic):
    '''Returns list of relevant site urls related to a `topic`'''
    try:
        topic = Topic.objects.get(name=topic)
        sites = [site.rss_url for site in topic.sites.all()]
        return sites

    except Topic.DoesNotExist:
        pass

def fetch_all_site_urls() -> tuple:
    '''Returns list of all site urls in the database.'''
    sites = [site for site in Site.objects.all()]
    return sites

def fetch_feed_and_save(urls: tuple):
    '''
    Fetch and store feed from the list of urls in the database.
    Takes urls tuple which is in format (site, <Topic Object>)
    '''
    posts = []
    for site,topic in urls:
        rss_url = site.rss_url
        parsed = feedparser.parse(rss_url)
        for entry in parsed["entries"]:
            title  = entry.get("title")
            link = entry.get("link")
            summary = entry.get("summary")
            published = entry.get("published")
            if published:
                published = dparser.parse(published, fuzzy=True)
            posts.append(Post(title=title, link=link, topic=topic, published=published,summary=summary, site=site))

    Post.objects.bulk_create(posts, ignore_conflicts=True)
    return True

all_sites = fetch_all_site_urls()
fetch_feed_and_save(all_sites)
