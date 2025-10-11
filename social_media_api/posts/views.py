from rest_framework import viewsets, permissions, generics
from rest_framework.filters import SearchFilter # Import SearchFilter
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


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


