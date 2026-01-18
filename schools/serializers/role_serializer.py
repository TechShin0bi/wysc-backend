from rest_framework import serializers
from ..models import Role

class RoleSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    school_name = serializers.CharField(source='school.name', read_only=True)
    campus_name = serializers.CharField(source='campus.name', read_only=True, allow_null=True)
    role_type_display = serializers.CharField(source='get_role_type_display', read_only=True)

    class Meta:
        model = Role
        fields = [
            'id', 'user', 'user_name', 'school', 'school_name',
            'campus', 'campus_name', 'role_type', 'role_type_display',
            'title', 'is_active', 'start_date', 'end_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = (
            'id', 'user_name', 'school_name', 'campus_name',
            'role_type_display', 'created_at', 'updated_at'
        )

    def get_user_name(self, obj):
        return f"{obj.user.get_full_name() or obj.user.username}"


class RoleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "school_type", "created_at", "updated_at"]
