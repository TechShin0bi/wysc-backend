from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Campus
from ..serializers import CampusSerializer, CampusDetailSerializer

class CampusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows campuses to be viewed or edited.
    """
    queryset = Campus.objects.select_related('school', 'address').all()
    serializer_class = CampusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['school', 'is_main_campus', 'is_active']
    search_fields = ['name', 'code', 'email', 'phone', 'school__name']
    ordering_fields = ['school__name', 'name', 'code']
    ordering = ['school__name', 'name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CampusDetailSerializer
        return CampusSerializer

    @action(detail=True, methods=['get'])
    def staff(self, request, pk=None):
        """
        Get all staff members for a specific campus.
        """
        from ..serializers import RoleSerializer
        campus = self.get_object()
        staff = campus.staff_roles.filter(is_active=True)
        serializer = RoleSerializer(staff, many=True, context={'request': request})
        return Response(serializer.data)
