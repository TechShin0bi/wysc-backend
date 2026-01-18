from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from .school import School
from .address import Address
from utils.models import BaseModel

class Campus(BaseModel):
    """Model representing a campus of a school."""
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='campuses',
        help_text=_("The school this campus belongs to")
    )
    name = models.CharField(max_length=255, help_text=_("Name of the campus"))
    code = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text=_("Unique code for the campus (e.g., MAIN, CAMPUS_A)")
    )
    address = models.OneToOneField(
        Address,
        on_delete=models.PROTECT,
        related_name='campus',
        help_text=_("Physical address of the campus")
    )
    phone = models.CharField(max_length=20, blank=True, null=True, help_text=_("Main contact number"))
    email = models.EmailField(blank=True, null=True, help_text=_("Main contact email"))
    is_main_campus = models.BooleanField(
        default=False,
        help_text=_("Is this the main campus of the school?")
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Campus")
        verbose_name_plural = _("Campuses")
        unique_together = [["school", "name"], ["school", "code"]]
        ordering = ["school", "name"]

    def __str__(self):
        return f"{self.school.name} - {self.name}"

    def save(self, *args, **kwargs):
        # Ensure only one main campus per school
        if self.is_main_campus:
            Campus.objects.filter(
                school=self.school, 
                is_main_campus=True
            ).exclude(pk=self.pk).update(is_main_campus=False)
        super().save(*args, **kwargs)
