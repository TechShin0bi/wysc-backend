from rest_framework import serializers
from ..models import Campus
from .address_serializer import AddressSerializer

class CampusSerializer(serializers.ModelSerializer):
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
        from ..models import Address
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        return Campus.objects.create(address=address, **validated_data)

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address_serializer.save()
        return super().update(instance, validated_data)
    

class CampusDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        exclude = ['created_at', 'updated_at']
