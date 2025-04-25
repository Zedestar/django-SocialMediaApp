import graphene
from posts import schema as post_schema
from chicken_disease_detection import schema



class Query(post_schema.Query, graphene.ObjectType):
    name = graphene.String(default_value="Come code with Zeddy")
    title = graphene.String(default_value="The Web and mobile developer")
    
    
    
    
schema = graphene.Schema(query=Query)