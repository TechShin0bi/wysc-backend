from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import BaseModel
from schools.models import Campus ,Address


class Person(BaseModel):
    """
    Base model for all person types in the system.
    """
    first_name = models.CharField(_('first name'), max_length=30)
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        if self.middle_name:
            full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        return full_name.strip()
    

class SchoolPerson(Person):
    """
    Model for a person associated with a school.
    """
    AVATAR_DEFAULT = 'avatars/default-avatar.png'
    AVATAR_UPLOAD_TO = 'avatars/'
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('U', _('Prefer not to say')),
    )
    
    avatar = models.ImageField(
        _('avatar'),
        upload_to=AVATAR_UPLOAD_TO,
        default=AVATAR_DEFAULT,
        blank=True,
        null=True
    )
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    email = models.EmailField(_('email address'), blank=True, null=True)
    gender = models.CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']