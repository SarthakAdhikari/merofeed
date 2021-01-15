import feedparser
import dateutil.parser as dparser
from feed.models import Site, Topic, Post

def fetch_site_urls_by_category(category):
    try:
        topic = Topic.objects.get(name=category)
        sites = [site.url for site in topic.sites.all()]
        return sites

    except Topic.DoesNotExist:
        pass

def fetch_all_site_urls() -> list:
    sites = [site.url for site in Site.objects.all()]
    return sites

def fetch_feed_from_all():
    sites = fetch_all_site_urls()
    posts = []
    for site in sites:
        parsed = feedparser.parse(site)
        for entry in parsed["entries"]:
            title  = entry.get("title")
            link = entry.get("link")
            published = entry.get("published")
            if published:
              published = dparser.parse(published, fuzzy=True)
            summary = entry.get("summary")
            posts.append(Post(title=title, link=link, published=published,summary=summary))

    saved_posts = Post.objects.bulk_create(posts, ignore_conflicts=True)
    return saved_posts

fetched_all = fetch_feed_from_all()
