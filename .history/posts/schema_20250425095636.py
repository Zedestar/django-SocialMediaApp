import graphene
from .models import Post
from graphene_django import DjangoObjectType

# - The schemas section

class PostType(DjangoObjectType):
    
    picture_url = graphene.String()
    class Meta:
        model = Post
        fields = "__all__"
        
    def resolve_picture_url(self, info):
        
class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    
    def resolve_posts(self, info):
        return Post.objects.all()