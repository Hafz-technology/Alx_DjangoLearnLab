from django.urls import path
from .views import CreateUserView, RetrieveUpdateProfileView, CustomAuthToken, FollowUserView


# Accounts End Points
urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('profile/', RetrieveUpdateProfileView.as_view(), name='profile'),
    path('follow/<int:pk>/', FollowUserView.as_view(), name='follow-user'),
]


# ["unfollow/<int:user_id>/", "follow/<int:user_id>"]

