# staff/factories.py
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.utils.text import slugify

from staff.models import Staff
from schools.models import Role, Campus
from schools.factories import CampusFactory as BaseCampusFactory

faker = Faker()

class RoleFactory(DjangoModelFactory):
    """Factory for creating Role instances."""
    class Meta:
        model = Role
        django_get_or_create = ('name',)

    name = factory.Faker('job')
    school_type = factory.Faker('random_element', elements=[t[0] for t in [
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('university', 'University')
    ]])
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Ensure the name is unique by appending a random string
        if 'name' in kwargs:
            kwargs['name'] = f"{kwargs['name']} {faker.lexify('???')}"
        return super()._create(model_class, *args, **kwargs)

class StaffFactory(DjangoModelFactory):
    """Factory for creating Staff instances."""
    class Meta:
        model = Staff
        # django_get_or_create = ('email',)  # Use email as the unique identifier
        skip_postgeneration_save = True

    # Personal Information
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    # email = factory.LazyAttribute(lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}@example.com")
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    phone_number = factory.Faker('phone_number')
    gender = factory.Faker('random_element', elements=['M', 'F', 'U'])
    
    # Relationships
    role = factory.SubFactory(RoleFactory)
    
    # Address will be created automatically by the Person model's save method
    address = factory.SubFactory('schools.factories.AddressFactory')
    
    # Campus is not a direct field on Staff, but we'll use it for related objects if needed
    # campus = None
    campus = factory.SubFactory('schools.factories.CampusFactory')
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Create the staff member
        staff = super()._create(model_class, *args, **kwargs)
        
        # If a campus was provided, update the address to be in that campus's location
        if 'campus' in kwargs and kwargs['campus']:
            staff.address = kwargs['campus'].address
            staff.save()
            
        return staff
        return super()._create(model_class, *args, **kwargs)