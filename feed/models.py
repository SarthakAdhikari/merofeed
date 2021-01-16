from django.db import models
from core.models import User
import tldextract

class Site(models.Model):
   rss_url = models.URLField()
   site_url = models.CharField(primary_key=True, max_length=200, unique=True, blank=True)

   def save(self, *args, **kwargs):
      if getattr(self, 'rss_url'):
         self.site_url = ".".join(part for part in tldextract.extract(self.rss_url) if part)
         super().save(*args,**kwargs)

   def __str__(self):
       return self.site_url

class Topic(models.Model):
    name = models.CharField(max_length=100)
    sites = models.ManyToManyField(Site)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    topic = models.ManyToManyField(Topic)


class Post(models.Model):
   title = models.CharField(max_length = 100)
   summary = models.TextField()
   link = models.URLField()
   published = models.DateTimeField()
   site = models.ForeignKey(Site, on_delete=models.CASCADE)

   def __str__(self):
       return f'{self.post_id} {self.title}'

# import feed.fetch
