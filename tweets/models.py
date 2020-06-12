from django.db import models
import random
from django.conf import settings

# uses default User Model
User = settings.AUTH_USER_MODEL

# Like Entity
class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE) # have to use quotes since TweetModel is below the tweet likes
    timestamp = models.DateTimeField(auto_now_add=True)

# Tweet Entity
# Blank=true, null=True makes so that it's not required to have data in db
class Tweet(models.Model):
    # can do this if we want null to happen when user is deleted
    # user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # OneToMany users can have many tweets - many tweets can have 1 user
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike) #one Tweet can have many Users, and one User can have many Tweets
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    # this method lets you have a say in how you want the Tweet object data to be displayed in AdminUI
    # def __str__(self):
    #     return self.content

    # will order descending order
    class Meta:
        ordering = ['-id']
    
    @property
    def is_retweet(self):
        return self.parent != None


    # ==== Old way or Serialilzing ===
    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "content": self.content,
    #         "likes": random.randint(0, 300)
    #     }
    


