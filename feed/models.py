from django.db import models
from core.models import User

class Site(models.Model):
   url = models.URLField()

   def __str__(self):
       return self.url

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


   def __str__(self):
       return f'{self.post_id} {self.title}'

import feed.fetch
