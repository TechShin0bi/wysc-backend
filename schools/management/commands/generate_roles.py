from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from schools.models import Role
from utils.const import SCHOOL_TYPES

class Command(BaseCommand):
    help = 'Generate standard roles for each school type'

    ROLES_BY_TYPE = {
        'primary': [
            ('headteacher', 'HT'),
            ('deputy_head', 'DHT'),
            ('class_teacher', 'CT'),
            ('assistant_teacher', 'AT'),
            ('administrator', 'Admin'),
        ],
        'secondary': [
            ('principal', 'PAL'),
            ('deputy_principal', 'DP'),
            ('head_of_department', 'HOD'),
            ('teacher', 'TCH'),
            ('librarian', 'LIB'),
            ('counselor', 'COUN'),
        ],
        'high_school': [
            ('principal', 'PAL'),
            ('vice_principal', 'VP'),
            ('dean_of_students', 'DOS'),
            ('head_of_department', 'HOD'),
            ('teacher', 'TCH'),
            ('counselor', 'COUN'),
        ],
        'college': [
            ('director', 'DIR'),
            ('deputy_director', 'DD'),
            ('head_of_department', 'HOD'),
            ('lecturer', 'LEC'),
            ('librarian', 'LIB'),
        ],
        'university': [
            ('vice_chancellor', 'VC'),
            ('deputy_vice_chancellor', 'DVC'),
            ('dean', 'DEAN'),
            ('head_of_department', 'HOD'),
            ('professor', 'PROF'),
            ('lecturer', 'LEC'),
            ('researcher', 'RES'),
        ],
        'other': [
            ('administrator', 'ADMIN'),
            ('staff', 'STAFF'),
            ('manager', 'MGR'),
        ]
    }

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for school_type, _ in SCHOOL_TYPES:
            roles = self.ROLES_BY_TYPE.get(school_type, [])
            
            for role_name, abbreviation in roles:
                # Convert role_name to title case for display
                display_name = role_name.replace('_', ' ').title()
                
                # Check if role already exists for this school type
                role, created = Role.objects.get_or_create(
                    name=display_name,
                    school_type=school_type,
                    defaults={'abbreviation': abbreviation}
                )
                
                # If role exists but abbreviation is different, update it
                if not created and role.abbreviation != abbreviation:
                    role.abbreviation = abbreviation
                    role.save()
                    updated_count += 1
                elif created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} and updated {updated_count} roles.'
            )
        )