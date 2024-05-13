from rest_framework.routers import DefaultRouter

from core.api.v1.users.views import UsersViewSet


router = DefaultRouter()
router.register("users-views", UsersViewSet, basename="users-views")


urlpatterns = [] + router.urls
