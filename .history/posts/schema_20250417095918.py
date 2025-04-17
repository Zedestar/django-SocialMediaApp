import graphene
from .models import Post
from graphene_django import DjangoObjectType

# - The schemas section

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("__all___")
        
class Query(graphene.ObjectType):
    posts = DjangoObjectType(PostType)
    
    def resolve_posts(self, info):
        return Post.objects.all()