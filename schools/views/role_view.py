from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from ..models import Role
from ..serializers import RoleSerializer

class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows roles to be viewed or edited.
    """
    queryset = Role.objects.select_related('user', 'school', 'campus').all()
    serializer_class = RoleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['school', 'campus', 'role_type', 'is_active']
    search_fields = [
        'user__first_name', 'user__last_name', 'user__email',
        'title', 'school__name', 'campus__name'
    ]
    ordering_fields = ['user__last_name', 'user__first_name', 'role_type']
    ordering = ['user__last_name', 'user__first_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by school_id if provided in query params
        school_id = self.request.query_params.get('school_id')
        if school_id:
            queryset = queryset.filter(school_id=school_id)
            
        # Filter by campus_id if provided in query params
        campus_id = self.request.query_params.get('campus_id')
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
            
        # Filter by user_id if provided in query params
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search for roles by user name, email, or title.
        """
        search_term = request.query_params.get('q', '').strip()
        if not search_term:
            return Response(
                {"detail": "Search term 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        queryset = self.get_queryset().filter(
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term) |
            Q(user__email__icontains=search_term) |
            Q(title__icontains=search_term)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
