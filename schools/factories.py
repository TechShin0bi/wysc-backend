import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.utils.text import slugify

from schools.models import School, Campus, Address

faker = Faker()

class AddressFactory(DjangoModelFactory):
    """Factory for creating Address instances."""
    class Meta:
        model = Address
        django_get_or_create = ('address_line', 'city', 'state_province')
    
    address_line = factory.LazyFunction(lambda: faker.street_address())
    address_line2 = factory.LazyFunction(lambda: faker.secondary_address())
    city = factory.LazyFunction(lambda: faker.city())
    state_province = factory.LazyFunction(lambda: faker.state())
    postal_code = factory.LazyFunction(lambda: faker.postcode())
    country = "Nigeria"


class SchoolFactory(DjangoModelFactory):
    """Factory for creating School instances."""
    class Meta:
        model = School
        django_get_or_create = ('name',)
    
    name = factory.LazyFunction(lambda: f"{faker.company()} {faker.company_suffix()}")
    short_name = factory.LazyAttribute(lambda obj: ''.join(word[0].upper() for word in obj.name.split()[:3]))
    motto = factory.LazyFunction(lambda: faker.catch_phrase())
    website = factory.LazyFunction(lambda: faker.url())
    phone = factory.LazyFunction(lambda: faker.phone_number())
    is_active = True


class CampusFactory(DjangoModelFactory):
    """Factory for creating Campus instances with unique codes."""
    class Meta:
        model = Campus
        django_get_or_create = ('code',)  # Ensure unique codes
        skip_postgeneration_save = True  # Prevent double save issues
    
    school = factory.SubFactory(SchoolFactory)
    name = factory.LazyFunction(lambda: f"{faker.city()} Campus")
    code = factory.Sequence(lambda n: f"CAMPUS_{n:03d}")
    address = factory.SubFactory(AddressFactory)
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Ensure the code is unique by appending a timestamp if needed
        from django.utils import timezone
        from django.db.utils import IntegrityError
        
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                # If this is not the first attempt, modify the code
                if attempt > 0:
                    kwargs['code'] = f"{kwargs.get('code', 'CAMPUS')}_{timezone.now().strftime('%H%M%S')}_{attempt}"
                return super()._create(model_class, *args, **kwargs)
            except IntegrityError:
                if attempt == max_attempts - 1:  # Last attempt
                    raise
                continue
    phone = factory.LazyFunction(lambda: faker.phone_number())
    email = factory.LazyFunction(lambda: faker.email())
    is_main_campus = False
    is_active = True

    @factory.post_generation
    def set_main_campus(self, create, extracted, **kwargs):
        """Set this campus as the main campus if specified."""
        if not create:
            return
            
        if extracted:
            self.is_main_campus = True
            self.save()

    @classmethod
    def create(cls, **kwargs):
        """Override to handle is_main_campus logic."""
        is_main = kwargs.pop('is_main_campus', False)
        campus = super().create(**kwargs)
        if is_main:
            campus.is_main_campus = True
            campus.save()
        return campus
