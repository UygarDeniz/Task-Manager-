from rest_framework import permissions
from tasks.models import Task
from .models import Team, TeamMembership

class IsTeamMember(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        team_id = view.kwargs.get('team_id')
       
        # Team Listing
        if team_id is None:
            return True  

        return TeamMembership.objects.filter(team=team_id, member=request.user.id).exists()
    
    def has_object_permission(self, request, view, obj):
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        if isinstance(obj, Team):
            return obj.members.filter(id=request.user.id).exists()

        # Check if the object is a TeamMembership instance
        if isinstance(obj, TeamMembership):
            return obj.team.members.filter(id=request.user.id).exists()
        
        if isinstance(obj, Task):
            return obj.team.members.filter(id=request.user.id).exists()
        
        return False
    
class IsTeamAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        team_id = view.kwargs.get('team_id')
        
        # Creating a new team
        if team_id is None and request.method in ["POST"]:
            return True
        
        return TeamMembership.objects.filter(team=team_id, member=request.user.id, is_admin=True).exists()
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        team_id = view.kwargs.get('team_id')
        return TeamMembership.objects.filter(team=team_id, member=request.user.id, is_admin=True).exists()
    
class IsTeamAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return IsTeamAdmin().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return IsTeamAdmin().has_object_permission(request, view, obj)

