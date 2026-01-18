from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend 
from ..models import School
from ..serializers import SchoolSerializer, SchoolDetailSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows schools to be viewed or edited.
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'short_name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolDetailSerializer
        return SchoolSerializer

    @action(detail=True, methods=['get'])
    def campuses(self, request, pk=None):
        """
        Get all campuses for a specific school.
        """
        from ..serializers import CampusSerializer
        school = self.get_object()
        campuses = school.campuses.all()
        serializer = CampusSerializer(campuses, many=True, context={'request': request})
        return Response(serializer.data)
