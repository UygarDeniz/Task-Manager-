from rest_framework import serializers
from .models import Team, TeamMembership

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", 'name', 'description', 'members', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        request = self.context.get('request')
        team = super().create(validated_data)
        TeamMembership.create_admin_membership(team, request.user)
        return team

class TeamMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = ["id", 'team', 'member', 'is_admin', 'created_at', 'updated_at']