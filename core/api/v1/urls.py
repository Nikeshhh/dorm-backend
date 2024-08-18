from django.urls import path, include

urlpatterns = [
    path("", include("core.api.v1.authentication.urls")),
    path("laundry/", include("core.api.v1.laundry.urls")),
    path("rooms/", include("core.api.v1.rooms.urls")),
    path("duties/", include("core.api.v1.duties.urls")),
    path("proposals/", include("core.api.v1.proposals.urls")),
    path("users/", include("core.api.v1.users.urls")),
]
