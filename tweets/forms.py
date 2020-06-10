from django import forms

from .models import Tweet

from django.conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

# The Meta class describes the entire form
class TweetForm(forms.ModelForm):
    # If we wanted to delcare the feils withing the content
    # we could do something like
    # content = forms.CharField()
    class Meta:
        model = Tweet
        fields = ['content']
    
    # validates length of tweet data
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return content