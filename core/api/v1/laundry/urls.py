from rest_framework.routers import DefaultRouter
from core.api.v1.laundry.views import LaundryRecordViewSet

router = DefaultRouter()

router.register('records', LaundryRecordViewSet, 'laundry_records')


urlpatterns = [
    
] + router.urls
