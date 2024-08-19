from rest_framework.routers import DefaultRouter

from core.api.v1.users.views import UsersViewSet


router = DefaultRouter()
router.register("", UsersViewSet, basename="users-viewset")


urlpatterns = [] + router.urls
