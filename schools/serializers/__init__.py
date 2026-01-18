from .address_serializer import AddressSerializer
from .school_serializer import SchoolSerializer, SchoolDetailSerializer
from .campus_serializer import CampusSerializer, CampusDetailSerializer
from .role_serializer import RoleSerializer, RoleDetailSerializer

__all__ = [
    'AddressSerializer',
    'SchoolSerializer', 'SchoolDetailSerializer',
    'CampusSerializer', 'CampusDetailSerializer',
    'RoleSerializer','RoleDetailSerializer'
]
