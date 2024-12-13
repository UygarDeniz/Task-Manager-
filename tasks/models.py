from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User

from teams.models import Team


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='tasks')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    deadline = models.DateTimeField()
    estimated_duration = models.IntegerField()  # Hours
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @classmethod
    def create_task(cls, 
                    team: Team, 
                    title: str, 
                    description: str, 
                    priority: str, 
                    deadline: datetime, 
                    estimated_duration: int) -> 'Task':
        task = cls.objects.create(
            team=team,
            title=title,
            description=description,
            priority=priority,
            deadline=deadline,
            estimated_duration=estimated_duration
        )
        return task
    
    def assign_assignee(cls, task, assignee: User) -> 'Task':
        task.assignee = assignee
        task.save()
        return task
    
    def __str__(self):
        return self.title
