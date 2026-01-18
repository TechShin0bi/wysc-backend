from django.db import models
from utils.models import SchoolPerson
from schools.models import Role
from utils.models.base_model import BaseModel
from django.contrib.auth import get_user_model


User = get_user_model()


class Staff(SchoolPerson):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff", null=True, blank=True)