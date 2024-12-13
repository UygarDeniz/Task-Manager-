from .views import ProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', ProfileViewSet)

urlpatterns = router.urls


