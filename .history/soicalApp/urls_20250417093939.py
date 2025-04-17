from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView


urlpatterns = [
    path("", include("posts.urls")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
    path("chattings/", include("chattings.urls")),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]

# urlpatterns += static(settings.STATIC_URL, document.root = settings.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
