from rest_framework import serializers
from .models import Address, School, Campus, Role


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for the Address model."""
    class Meta:
        model = Address
        fields = [
            'id', 'address_line1', 'address_line2', 'city',
            'state_province', 'postal_code', 'country',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')


class SchoolSerializer(serializers.ModelSerializer):
    """Serializer for the School model."""
    class Meta:
        model = School
        fields = [
            'id', 'name', 'short_name', 'motto', 'website',
            'email', 'phone', 'logo', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')


class CampusSerializer(serializers.ModelSerializer):
    """Serializer for the Campus model with nested address."""
    address = AddressSerializer()
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = Campus
        fields = [
            'id', 'school', 'school_name', 'name', 'code', 'address',
            'phone', 'email', 'is_main_campus', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'school_name')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        campus = Campus.objects.create(address=address, **validated_data)
        return campus

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            address_serializer = self.fields['address']
            address_serializer.update(instance.address, address_data)

        return super().update(instance, validated_data)


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for the Role model with nested user and campus info."""
    user_name = serializers.SerializerMethodField()
    school_name = serializers.CharField(source='school.name', read_only=True)
    campus_name = serializers.CharField(source='campus.name', read_only=True)
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


class CampusDetailSerializer(CampusSerializer):
    """Extended Campus serializer with related roles."""
    roles = RoleSerializer(many=True, read_only=True, source='staff_roles')

    class Meta(CampusSerializer.Meta):
        fields = CampusSerializer.Meta.fields + ['roles']


class SchoolDetailSerializer(SchoolSerializer):
    """Extended School serializer with related campuses and roles."""
    campuses = CampusSerializer(many=True, read_only=True, source='campuses.all')
    roles = RoleSerializer(many=True, read_only=True, source='staff_roles')

    class Meta(SchoolSerializer.Meta):
        fields = SchoolSerializer.Meta.fields + ['campuses', 'roles']
