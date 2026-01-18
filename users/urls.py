from django.urls import path
from . views import UserAuthenticationView
urlpatterns = [
    path('login/', UserAuthenticationView.as_view(), name='login')
]