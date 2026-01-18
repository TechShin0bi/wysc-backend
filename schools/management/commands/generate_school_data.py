from django.core.management.base import BaseCommand
from schools.factories import SchoolFactory, CampusFactory

class Command(BaseCommand):
    help = 'Generate test data for schools and campuses'

    def add_arguments(self, parser):
        parser.add_argument(
            '--schools',
            type=int,
            default=2,
            help='Number of schools to create (default: 2)'
        )
        parser.add_argument(
            '--campuses',
            type=int,
            default=3,
            help='Number of campuses to create per school (default: 3)'
        )

    def handle(self, *args, **options):
        num_schools = options['schools']
        num_campuses = options['campuses']

        self.stdout.write(self.style.SUCCESS(f'Creating {num_schools} schools with {num_campuses} campuses each...'))

        for i in range(num_schools):
            # Create a school
            school = SchoolFactory()
            self.stdout.write(self.style.SUCCESS(f'Created school: {school.name}'))

            # Create campuses for the school
            for j in range(num_campuses):
                is_main = (j == 0)  # First campus is main
                campus = CampusFactory(
                    school=school,
                    is_main_campus=is_main,
                    name=f"{school.name.split()[0]} Campus {j+1}"
                )
                campus_type = "Main" if is_main else "Regular"
                self.stdout.write(
                    self.style.SUCCESS(f'  - Created {campus_type.lower()} campus: {campus.name} (Code: {campus.code})')
                )

        self.stdout.write(self.style.SUCCESS('\nTest data generation complete!'))
        self.stdout.write(self.style.SUCCESS('You can now check your admin interface to see the generated data.'))