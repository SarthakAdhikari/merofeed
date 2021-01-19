import feedparser
import dateutil.parser as dparser
from feed.models import Site, Topic, Post, Subscription
from feed.serializers import PostSerializer

class Feed:
    @staticmethod
    def fetch_site_urls_by_topic(topic):
        '''Returns list of relevant site urls related to a `topic`'''
        try:
            topic = Topic.objects.get(name=topic)
            sites = [site.url for site in topic.sites.all()]
            return sites

        except Topic.DoesNotExist:
            pass

    @staticmethod
    def fetch_all_site_urls(self) -> list:
        '''Returns list of all site urls in the database.'''
        sites = [site.url for site in Site.objects.all()]
        return sites

    @staticmethod
    def fetch_feed_and_save(urls: list):
        '''Fetch and store feed from the list of urls urls in the database.'''
        posts = []
        for site in urls:
            parsed = feedparser.parse(site)
            for entry in parsed["entries"]:
                title  = entry.get("title")
                link = entry.get("link")
                published = entry.get("published")
                if published:
                    published = dparser.parse(published, fuzzy=True)
                    summary = entry.get("summary")
                    posts.append(Post(title=title, link=link, published=published,summary=summary))

        Post.objects.bulk_create(posts, ignore_conflicts=True)
        return True

class UserFeed(Feed):

    def __init__(self,user):
        self.user = user
        self.topics = self.get_user_topics()
        self.feed = {"feed": { "topics": [], "data": {}}}

    def get_user_topics(self):
        if self.user.pk:
            return [topic for topic in Subscription.objects.get(user=self.user).topic.all()]

    def generate_user_feed(self):
        for topic in self.topics:
            posts = Post.objects.filter(topic=topic).order_by('-published')[:4]
            all_post = PostSerializer(posts, many=True)
            self.feed["feed"]["topics"].append(topic.name)
            self.feed["feed"]["data"][topic.name] = all_post.data


    def get_user_feed(self):
        self.generate_user_feed()
        return self.feed
