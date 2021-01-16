from rest_framework import generics
from rest_framework.views import APIView

class FeedView(APIView):
    def get(self, request, *args, **kwargs):
       user = request.user
       pass
