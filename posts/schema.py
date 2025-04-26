import graphene
from .models import Post, Comment
from graphene_django import DjangoObjectType

# - The schemas section

class PostType(DjangoObjectType):

    picture_url = graphene.String()
    class Meta:
        model = Post
        fields = [
            "id", 
            "user", 
            "picture_url",
            "title",
            "caption",
            "viewers", 
            # "comments",
            "likes", 
            "dislikes", 
            "bookmark", 
            "created_at", 
            "updated_at",
            ]
        
    def resolve_picture_url(self, info):
        if self.photo:
            return info.context.build_absolute_uri(self.photo.url)
        
class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ["post", "user", "body", "created_at"]
        
class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    comments = graphene.List(CommentType)
    
    def resolve_posts(self, info):
        return Post.objects.all()
    
    def resolve_comments(self, info):
        return Comment.objects.all()