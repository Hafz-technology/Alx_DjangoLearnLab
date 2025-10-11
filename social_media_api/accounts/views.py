from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import User
from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from notifications.models import Notification



# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class RetrieveUpdateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomAuthToken(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        })


class FollowUserView(APIView):    # , generics.GenericAPIView
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, format=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        current_user = request.user

        if current_user == user_to_follow:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        current_user.following.add(user_to_follow)
        Notification.objects.create(
            recipient=user_to_follow,
            actor=current_user,
            verb='started following you',
            target=current_user # The target is the user who initiated the follow
        )
        
        return Response({'status': f'Successfully followed {user_to_follow.username}'}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, format=None):
        user_to_unfollow = get_object_or_404(User, pk=pk)
        current_user = request.user

        current_user.following.remove(user_to_unfollow)
        return Response({'status': f'Successfully unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
        
