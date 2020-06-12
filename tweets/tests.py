from django.test import TestCase
from .models import Tweet
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

# Create your tests here.
User = get_user_model()
class TweetTestCase(TestCase):
    # ==== Notes for Myself on Tests ===
    # Function that aren't being tested need to be written as CamelCase instead of snake case
    def setUp(self):
        # User.objects.create_user(username='abc', password='somepassword')
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        Tweet.objects.create(user=self.user, content='my 1stt tweet')
        Tweet.objects.create(user=self.user, content='my 2nd tweet')
        Tweet.objects.create(user=self.user, content='my 3rd tweet')
        self.currentCount = Tweet.objects.all().count()
         
    def test_user_exists(self):
        # user = User.objects.get(username='cfe')
        self.assertEqual(self.user.username, 'cfe')

    # ==== Notes for Myself on Tests ===
    # Need to define each one as a function with 'test_' at the start of the name
    # create your objects to run and then assertEqual to test correct info
    # use command `./manage.py test`
    def test_tweet_created(self):
        tweet = Tweet.objects.create(user=self.user, content='my 4th tweet')
        self.assertEqual(tweet.user, self.user)
        self.assertEqual(tweet.id, 10)
        self.assertEqual(tweet.content, 'my 4th tweet')
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client
    
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        # print(response.json())
    
    def test_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/',{"id": 1,"action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 1)
        # print(response.json())
    
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/',{"id": 2,"action": "like"})
        self.assertEqual(response.status_code, 200)
        # like_count = response.json().get('likes')
        # self.assertEqual(like_count, 1)

        response = client.post('/api/tweets/action/',{"id": 2,"action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 0)
    
    def test_action_retweet(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/',{"id": 2,"action": "retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual(self.currentCount + 1, new_tweet_id)
    
    def test_tweet_create_api_view(self):
        request_data = {"content": "this is a new tweet"}
        client = self.get_client()
        response = client.post('/api/tweets/create/',{"id": 2,"action": "retweet"})
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get('id')
        self.assertEqual(self.currentCount + 1, new_tweet_id)
    

    # Will need to look into what kinds of Tests is critical at first
    # look into any specific libraries then using build in test in django
        