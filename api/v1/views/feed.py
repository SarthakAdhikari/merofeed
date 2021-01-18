from rest_framework import generics
from rest_framework.views import APIView

from feed.models import Topic, Subscription
from feed.serializers import SubscriptionSerializer
from feed.services import UserFeed

from rest_framework.response import Response

class SubscriptionView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer


class FeedView(APIView):
    def get(self, request, *args, **kwargs):
        user_feed = UserFeed(request.user)
        return Response(user_feed.get_user_feed())
