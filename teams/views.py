from rest_framework import viewsets
from .models import Team, TeamMembership
from .serializers import TeamSerializer, TeamMembershipSerializer
from .permissions import IsTeamMember, IsTeamAdminOrReadOnly

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsTeamMember, IsTeamAdminOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        return Team.objects.filter(members=user)

class TeamMembershipViewSet(viewsets.ModelViewSet):
    queryset = TeamMembership.objects.all()
    serializer_class = TeamMembershipSerializer
    permission_classes = [IsTeamMember, IsTeamAdminOrReadOnly]
    
    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return TeamMembership.objects.filter(team_id=team_id)



        
    
    
    
