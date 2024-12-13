from django.contrib.auth.models import User
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, through='TeamMembership', related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['team', 'member']
    
    @classmethod
    def create_admin_membership(cls, team: Team, member: User) -> 'TeamMembership':
        return cls.objects.create(team=team, member=member, is_admin=True)
    
    def __str__(self):
        return f"{self.member.username} in {self.team.name} (Admin: {self.is_admin})"