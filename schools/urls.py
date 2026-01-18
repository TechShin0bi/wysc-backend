from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for our viewsets
router = DefaultRouter()
router.register(r'addresses', views.AddressViewSet)
router.register(r'schools', views.SchoolViewSet)
router.register(r'campuses', views.CampusViewSet)
router.register(r'roles', views.RoleViewSet)

app_name = 'schools'

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]
