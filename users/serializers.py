from rest_framework import serializers
from .models import  Profile



class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user', read_only=True)
    
    class Meta:
        model = Profile
        fields = ["id", "user_id", "username", 'workload_capacity']