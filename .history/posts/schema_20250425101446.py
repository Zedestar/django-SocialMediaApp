import graphene
from .models import Post
from graphene_django import DjangoObjectType

# - The schemas section

class PostType(DjangoObjectType):
    
    picture_url = graphene.String()
    class Meta:
        model = Post
        fields = ["id", "user", "picture_url", "caption", "viewers", "likes", "dislikes", "bookmark", "created_at"]
        
    def resolve_picture_url(self, info):
        if self.photo:
            return info.context.build_absolute
        
class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    
    def resolve_posts(self, info):
        return Post.objects.all()