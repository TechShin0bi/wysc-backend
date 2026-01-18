from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import BaseModel
from utils.const import SCHOOL_TYPES



class School(BaseModel):
    """Model representing a school."""
    
    
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=50, blank=True, null=True, 
                                help_text=_("Short name or abbreviation"))
    school_type = models.CharField(max_length=50, blank=True, null=True,
                                choices=SCHOOL_TYPES,
                                default=SCHOOL_TYPES[0][0],
                                help_text=_("Type of school (e.g., Primary, Secondary, High School)"))
    motto = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='schools/logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")
        ordering = ["name"]

    def __str__(self):
        return self.name
