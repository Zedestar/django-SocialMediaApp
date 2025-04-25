import graphene
from posts import schema
from 



class Query(schema.Query, graphene.ObjectType):
    name = graphene.String(default_value="Come code with Zeddy")
    title = graphene.String(default_value="The Web and mobile developer")
    
    
    
    
schema = graphene.Schema(query=Query)