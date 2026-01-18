from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import BaseModel

class Address(BaseModel):
    """Model to store address information for schools and campuses."""
    address_line = models.CharField(max_length=255, help_text=_("Street address, P.O. box"))
    address_line2 = models.CharField(max_length=255, blank=True, null=True, 
                                   help_text=_("Apartment, suite, unit, building, floor, etc."))
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, help_text=_("State/Province/Region"))
    postal_code = models.CharField(max_length=20, help_text=_("ZIP/Postal code") , blank=True, null=True)
    country = models.CharField(max_length=100, default="CM", blank=True, null=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        ordering = ["country", "state_province", "city"]

    def __str__(self):
        return f"{self.address_line}, {self.city}, {self.state_province}, {self.country}"
