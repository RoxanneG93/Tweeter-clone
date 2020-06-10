from django.contrib import admin

# Register your models here.
from .models import Tweet, TweetLike


class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike

# here we are customizing the admin page search for Tweets
# so we can look/filter for specific Tweets bases on specified search field
class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['user__username', 'user__email']
    class Meta:
        model = Tweet

admin.site.register(Tweet, TweetAdmin)