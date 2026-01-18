from rest_framework import serializers
from .models import Staff
from schools.serializers import CampusDetailSerializer , RoleDetailSerializer


class StaffDetailSerializer(serializers.ModelSerializer):
    campus = CampusDetailSerializer(read_only=True)
    role = RoleDetailSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    class Meta:
        model = Staff
        fields = ['id', 'user', 'campus', 'role', 'full_name', 'created_at', 'updated_at']
