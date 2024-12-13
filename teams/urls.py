from rest_framework import routers
from django.urls import path, include
from .views import TeamViewSet, TeamMembershipViewSet

router = routers.DefaultRouter()
router.register(r'', TeamViewSet)
router.register(r'(?P<team_id>\d+)/memberships', TeamMembershipViewSet)


urlpatterns = [
    path("<int:team_id>/tasks/", include("tasks.urls")),
    path("", include(router.urls))
]