from rest_framework import generics
from rest_framework.views import APIView

from feed.models import Topic, Subscription
from feed.serializers import SubscriptionSerializer

class SubscriptionView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class FeedView(APIView):
    def get(self, request, *args, **kwargs):
        topics = [topic.name for topic in Subscription.objects.get(user=request.user).topic.all()]
