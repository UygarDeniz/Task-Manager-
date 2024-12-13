from rest_framework.viewsets import ModelViewSet
from .models import Profile
from .serializers import ProfileSerializer
from .permissions import IsProfileOwner


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwner]

