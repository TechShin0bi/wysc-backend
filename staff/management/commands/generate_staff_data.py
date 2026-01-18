from django.core.management.base import BaseCommand
from django.db import transaction
from staff.factories import RoleFactory, StaffFactory

class Command(BaseCommand):
    help = 'Create sample staff and roles for testing/development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--roles',
            type=int,
            default=5,
            help='Number of roles to create (default: 5)'
        )
        parser.add_argument(
            '--staff',
            type=int,
            default=10,
            help='Number of staff members to create (default: 10)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing staff and roles before creating new ones'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        num_roles = options['roles']
        num_staff = options['staff']
        clear = options['clear']

        # Import models here to avoid circular imports
        from staff.models import Staff, Role

        if clear:
            self.stdout.write('Clearing existing staff and roles...')
            Staff.objects.all().delete()
            Role.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleared existing data'))

        self.stdout.write(f'Creating {num_roles} roles...')
        roles = RoleFactory.create_batch(num_roles)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(roles)} roles'))

        self.stdout.write(f'Creating {num_staff} staff members...')
        staff_members = StaffFactory.create_batch(num_staff)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(staff_members)} staff members'))

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(roles)} roles and {len(staff_members)} staff members!'
            )
        )
