from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Address
from ..serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows addresses to be viewed or edited.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['address_line1', 'address_line2', 'city', 'state_province', 'postal_code', 'country']
    ordering_fields = ['country', 'state_province', 'city']
    ordering = ['country', 'state_province', 'city']
