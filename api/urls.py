from django.urls import path
from rest_framework import routers

from api.v1.views.core import CreateUserView, LoginView
from api.v1.views.feed import FeedView

urlpatterns = [
    path('login/', LoginView.as_view() , name="login"),
    path('signup/', CreateUserView.as_view(), name="signup"),
    path('feed/', FeedView.as_view(), name="feed")
]
