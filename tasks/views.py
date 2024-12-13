from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from teams.models import Team
from .models import Task
from .serializers import TaskSerializer
from teams.permissions import IsTeamMember, IsTeamAdmin

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTeamMember]
    
    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        return Task.objects.filter(team_id=team_id)
    
    def perform_create(self, serializer):
        team_id = self.kwargs['team_id']
        
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            raise PermissionDenied(detail="Team does not exist") 
        
        # Check if the user has permission to create a task in the team (only Admin)
        if not IsTeamAdmin().has_permission(self.request, self):
            raise PermissionDenied(detail="Only team admins can create new tasks")
        
        serializer.save(team=team)
    
    def perform_update(self, serializer):
        # Check if the user has permission to update the task (only Admin and Assigned User)
        user = self.request.user
        task = self.get_object()
        assigned_user = task.assignee
        is_admin = IsTeamAdmin().has_object_permission(self.request, self, task)
        
        if user != assigned_user and not is_admin:
            raise PermissionDenied(detail="Only the assigned user or team admins can update the task")
            
        serializer.save()
    
    @action(detail=True, methods=['patch'], permission_classes=[IsTeamAdmin])
    def assign_assignee(self, request, team_id=None, pk=None):
        """
        Custom action to assign a new assignee to a task.
        """
        task = self.get_object()
        assignee_id = request.data.get('assignee')

        if not assignee_id:
            return Response(
                {"detail": "Assignee ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            assignee = User.objects.get(id=assignee_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        task.assign_assignee(task, assignee)
        serializer = self.get_serializer(task)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        

