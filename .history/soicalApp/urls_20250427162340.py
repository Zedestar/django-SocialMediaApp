from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from chicken_disease_detection.views import PredictDiseaseAPIView


urlpatterns = [
    path("", include("posts.urls")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
    path("chattings/", include("chattings.urls")),
    path("chicken/", include("chicken_disease_detection.urls")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("predict/", PredictDiseaseAPIView.as_view)
]

# urlpatterns += static(settings.STATIC_URL, document.root = settings.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
