from rest_framework import serializers
from ..models import School, Campus
from .campus_serializer import CampusSerializer

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'id', 'name', 'short_name', 'motto', 'website',
            'email', 'phone', 'logo', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

class SchoolDetailSerializer(SchoolSerializer):
    campuses = serializers.SerializerMethodField()

    class Meta(SchoolSerializer.Meta):
        fields = SchoolSerializer.Meta.fields + ['campuses']

    def get_campuses(self, obj):
        campuses = obj.campuses.all()
        return CampusSerializer(campuses, many=True, context=self.context).data
