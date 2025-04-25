import graphene
from posts import schema as post_schema
from chicken_disease_detection import schema as chicken_schema



class Query(post_schema.Query, graphene.ObjectType):
    name = graphene.String(default_value="Come code with Zeddy")
    title = graphene.String(default_value="The Web and mobile developer")
    
    
class Mutation(chicken_schema.Mutation):
    pass
    
    
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)