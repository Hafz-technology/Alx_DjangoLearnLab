from rest_framework import viewsets, permissions, generics
from rest_framework.filters import SearchFilter 
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from notifications.models import Notification 



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at') # Order by newest first
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter] # Add this
    search_fields = ['title', 'content'] # Add fields you want to search by

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# ... CommentViewSet remains the same
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Create notification for the post author
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on',
                target=comment.post
            )



class FeedView(generics.ListAPIView):
    """
    This view returns a personalized feed of posts from users 
    that the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This method generates the queryset for the feed.
        """
        current_user = self.request.user
        # Get all the user objects that the current user is following.
        following_users = current_user.following.all()
        
        # This is the line you're looking for. It filters the posts...
        # ...to only include authors in the `following_users` list
        # and then orders them by the newest first.
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if Like.objects.filter(user=user, post=post).exists():
            return Response({'error': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(user=user, post=post)
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked',
                target=post
            )
            
        return Response({'status': 'Post liked'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        like = Like.objects.filter(user=user, post=post)
        if like.exists():
            like.delete()
            return Response({'status': 'Post unliked'}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({'error': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
