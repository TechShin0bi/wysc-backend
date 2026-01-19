from django.urls import path
from . views import UserAuthenticationView, MeView

urlpatterns = [
    path('login/', UserAuthenticationView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
]
