from django.core.management.base import BaseCommand
from login.models import LoginStudent, TeacherAdmin

class Command(BaseCommand):
    help = 'Creates a new user (student or teacher)'

    def add_arguments(self, parser):
        parser.add_argument('--type', type=str, choices=['student', 'teacher'], required=True,
                          help='Type of user to create (student or teacher)')
        parser.add_argument('--username', type=str, required=True,
                          help='Username for the user')
        parser.add_argument('--email', type=str, required=True,
                          help='Email for the user')
        parser.add_argument('--password', type=str, required=True,
                          help='Password for the user')
        parser.add_argument('--dept', type=str, required=True,
                          help='Department code')
        parser.add_argument('--year', type=int, required=False,
                          help='Year (required for students)')

    def handle(self, *args, **options):
        user_type = options['type']
        username = options['username']
        email = options['email']
        password = options['password']
        dept = options['dept']
        
        try:
            if user_type == 'student':
                if not options['year']:
                    self.stdout.write(self.style.ERROR('Year is required for students'))
                    return
                
                user = LoginStudent.objects.create(
                    username=username,
                    password=password,  # In production, use proper password hashing
                    emailid=email,
                    dept=dept,
                    year=options['year']
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created student "{username}"'))
            
            else:  # teacher
                user = TeacherAdmin.objects.create(
                    username=username,
                    password=password,  # In production, use proper password hashing
                    emailid=email,
                    dept=dept,
                    usertype='teacher'
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created teacher "{username}"'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {str(e)}')) 