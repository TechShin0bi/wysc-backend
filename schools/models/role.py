from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import BaseModel
from utils.const import SCHOOL_TYPES

class Role(BaseModel):
    """Model representing user roles within a school/campus.""" 
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Custom title for the role (if not covered by role type)")
    )
    abbreviation = models.CharField(_("abbreviation"), max_length=50)
    
    school_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=SCHOOL_TYPES,
        default=SCHOOL_TYPES[0][0],
        help_text=_("The school type this role is associated with (if applicable)")
    )

    class Meta:
        verbose_name = _("Role")
        db_table = 'roles'
        verbose_name_plural = _("Roles")
        ordering =  ["name"]

    def __str__(self):
        role_display = self.name 
        if self.school_type:
            role_display += f" ({self.school_type})"
        return f"{role_display}"
