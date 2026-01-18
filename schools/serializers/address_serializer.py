from rest_framework import serializers
from ..models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'address_line1', 'address_line2', 'city',
            'state_province', 'postal_code', 'country',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')
