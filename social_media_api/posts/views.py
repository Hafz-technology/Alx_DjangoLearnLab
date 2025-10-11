from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter # Import SearchFilter
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics

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
        serializer.save(author=self.request.user)


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the posts
        by users that the currently authenticated user follows.
        """
        current_user = self.request.user
        followed_users = current_user.following.all()
        
        # Filter posts to only include those from followed users
        # and order them by the most recent
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')     
    
    
    
