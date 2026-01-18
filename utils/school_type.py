from django.db import models

class SchoolType(models.Choice):
    PRIVATE = 'private'
    PUBLIC = 'public'
    
    class Meta:
        verbose_name = 'School Type'
        verbose_name_plural = 'School Types'

class InstituteType(models.Choice):
    PROFESSIONAL = 'professional'
    TECHNICAL = 'technical'
    