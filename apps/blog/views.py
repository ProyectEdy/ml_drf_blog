from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

from .models import Post, Heading, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer,PostView
from .utils import get_client_ip

"""class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer"""

class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            posts = Post.postobjects.all()

            if not posts.exists():
                raise NotFound(detail="No posts found")

            serialized_posts = PostListSerializer(posts, many=True).data
        except Post.DoesNotExist:
            raise NotFound(detail="Not post found.")
        
        return Response(serialized_posts)

"""class PostDetailView(RetrieveAPIView):
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'"""

class PostDetailView(RetrieveAPIView):
    def get(self, request, slug): 
        try:
            post = Post.postobjects.get(slug=slug)
        except Post.DoesNotExist:
            
            raise NotFound(detail="The requested post does not exist")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurreed: {str(e)}")
        
        serialized_post = PostSerializer(post).data

        #Esto incrementa el contador de vistas 
        try:
            post_analytics = PostAnalytics.objects.get(post=post)
            post_analytics.increment_view(request)
        except PostAnalytics.DoesNotExist:
            raise NotFound(detail="Analytics data for this post does not exist")
        except Exception as e:
            raise APIException(detail=f"An error ocurred while updating post analytics: {str(e)}")
        
        return Response(serialized_post)


class PostHeadingsView(ListAPIView):
    serializer_class = HeadingSerializer

    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Heading.objects.filter(post__slug = post_slug)
    

class IncrementPostClickView(APIView):
  
    def post(self, request):
        """
        Incrementa un contador de clicks basado en su slug
        """
        data = request.data

        try:
            post = Post.postobjects.get(slug=data['slug'])
        except Post.DoesNotExist:
            
            raise NotFound(detail="The requested post does not exist")

        try:
            post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
            post_analytics.increment_click()
        except Exception as e:
            raise APIException(detail=f"An error ocurred while updating post analytics: {str(e)}")
        return Response({
            "message": "Click increment successfully",
            "clicks": post_analytics.clicks
        })