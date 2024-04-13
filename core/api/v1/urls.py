from django.urls import path, include

urlpatterns = [
    path("app_example/", include("core.api.v1.app_example.urls")),
]
