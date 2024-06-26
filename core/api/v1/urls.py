from django.urls import path, include

urlpatterns = [
    path("app_example/", include("core.api.v1.app_example.urls")),
    path("", include("core.api.v1.authentication.urls")),
    path("laundry/", include("core.api.v1.laundry.urls")),
    path("rooms/", include("core.api.v1.rooms.urls")),
    path("duties/", include("core.api.v1.duties.urls")),
    path("proposals/", include("core.api.v1.proposals.urls")),
    path("users/", include("core.api.v1.users.urls")),
]
