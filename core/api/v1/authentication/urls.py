from rest_framework.routers import DefaultRouter
from .views import AuthenticationViewSet

router = DefaultRouter()

router.register('auth', AuthenticationViewSet, 'authentication')


urlpatterns = [
    
] + router.urls
