import graphene



class Query(graphene.ObjectType):
    name = graphene.String(default_value="Come code with Zeddy")
    
    
    
    
schema = graphene.Schema(query=Query)