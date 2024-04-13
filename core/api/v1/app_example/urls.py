from django.urls import path
from core.api.v1.app_example.views import hello_world_view

urlpatterns = [path("hello/", hello_world_view)]
