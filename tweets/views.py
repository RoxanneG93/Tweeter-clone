import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet
from .forms import TweetForm
from django.utils.http import is_safe_url
from .serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    # args and kwaregs are parameters grabbed from the url
    # print(args, kwargs)
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


# changing create Tweet view to using the REST framework
@api_view(['POST']) # http method the client needs to send is POST
# @authentication_classes([SessionAuthentication, CustomeClass])  #adds that only session Auth is valid, then passes to role permission
@permission_classes([IsAuthenticated]) # **Check out the RES API course for better detail on Class based views and better Auth role handling
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    # print(request.POST)
    # print(request.user)
    print(request.data)

    '''
    id is required.
    Actions options are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')

        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == 'like':
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'retweet':
            new_tweet = Tweet.objects.create(
                user=request.user, 
                parent=obj,
                content=content,
                )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)

    # qs = qs.filter(user=request.user)
    # if not qs.exists():
    #     return Response({"message": "You cannot delete this tweet"}, status=401)
    return Response({}, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):

    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)

    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)

    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet deleted"}, status=200)


# Previous view with pure django
def tweet_create_view_pure_django(request, *args, **kwargs):

    # pass Post Data to Form or none
    # print('post data is', request.POST)
    # print("ajax", request.is_ajax())
    # print('login_url', settings.LOGIN_URL) #  default is - /accounts/login/

    user = request.user
    # print("user", user)
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            #  not authorized response
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    next_url = request.POST.get('next') or None
    form = TweetForm(request.POST or None)
    if form.is_valid():
        # what is commit false mean? - stops form model from saving before user is added
        # and to allow us to save by the model later on like so:
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
       
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 === created items
        # if next url is not an allowed host, then it will redirect to create-tweet page -- magically? <.<
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)

# Or we can just grab accept parameter like so:
def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by Javascript, React, IOS, etc
    return json data
    """
    data = {
        "id": tweet_id,
        # "image_path": obj.image.url
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
         data['message'] = "Not Found"
         status = 404
        # return HttpResponse(f"<h1>Error, cannot find Twee with id: { tweet_id }</h1>")
    return JsonResponse(data, status=status) #json.dumps content_type='application.json'


# Additional Notes for myself
# obj.likes.add()
# obj.likes.remove()
# obj.likes.set() #requires a queryset
# User.objects.mone() - empty queryset