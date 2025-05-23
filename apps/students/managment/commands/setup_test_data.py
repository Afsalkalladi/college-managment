# Create directory: students/management/commands/
# Create file: students/management/commands/setup_test_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import TeacherProfile, StudentProfile
from academics.models import Scheme, AcademicYear, Semester, Subject
from teachers.models import TeacherAssignment
from students.models import StudentEnrollment
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test data for the college management system'
    
    def handle(self, *args, **kwargs):
        # Create academic year
        academic_year, _ = AcademicYear.objects.get_or_create(
            year='2024-2025',
            defaults={
                'start_date': date(2024, 7, 1),
                'end_date': date(2025, 6, 30),
                'is_current': True
            }
        )
        
        # Create scheme
        scheme, _ = Scheme.objects.get_or_create(
            name='2023',
            defaults={'start_year': 2023, 'is_active': True}
        )
        
        # Create semesters
        for i in range(1, 9):
            Semester.objects.get_or_create(
                scheme=scheme,
                number=i,
                defaults={'name': f'Semester {i}'}
            )
        
        # Create sample subjects for first semester
        semester1 = Semester.objects.get(scheme=scheme, number=1)
        subjects = [
            {'code': 'CS101', 'name': 'Programming Fundamentals', 'credits': 4},
            {'code': 'CS102', 'name': 'Data Structures', 'credits': 4},
            {'code': 'CS103', 'name': 'Database Management', 'credits': 3},
            {'code': 'CS104', 'name': 'Web Technologies', 'credits': 3},
        ]
        
        for subj in subjects:
            Subject.objects.get_or_create(
                code=subj['code'],
                defaults={
                    'name': subj['name'],
                    'scheme': scheme,
                    'semester': semester1,
                    'credits': subj['credits']
                }
            )
        
        # Create a test teacher
        teacher_user, _ = User.objects.get_or_create(
            username='teacher1',
            defaults={
                'email': 'teacher1@college.edu',
                'user_type': 'teacher',
                'first_name': 'John',
                'last_name': 'Doe',
                'is_verified': True
            }
        )
        teacher_user.set_password('password123')
        teacher_user.save()
        
        teacher_profile, _ = TeacherProfile.objects.get_or_create(
            user=teacher_user,
            defaults={
                'employee_id': 'EMP001',
                'qualification': 'M.Tech Computer Science',
                'specialization': 'Data Structures and Algorithms'
            }
        )
        
        # Create a test student
        student_user, _ = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@college.edu',
                'user_type': 'student',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'is_verified': True
            }
        )
        student_user.set_password('password123')
        student_user.save()
        
        student_profile, _ = StudentProfile.objects.get_or_create(
            user=student_user,
            defaults={
                'roll_number': 'CS2023001',
                'admission_year': 2023,
                'current_semester': 1
            }
        )
        
        # Create enrollments
        StudentEnrollment.objects.get_or_create(
            student=student_profile,
            academic_year=academic_year,
            defaults={
                'scheme': scheme,
                'current_semester': semester1,
                'is_active': True
            }
        )
        
        # Assign teacher to subjects
        for subject in Subject.objects.filter(semester=semester1):
            TeacherAssignment.objects.get_or_create(
                teacher=teacher_profile,
                subject=subject,
                academic_year=academic_year,
                defaults={'is_active': True}
            )
        
        self.stdout.write(self.style.SUCCESS('Test data created successfully!'))
        self.stdout.write('Teacher login: username=teacher1, password=password123')
        self.stdout.write('Student login: username=student1, password=password123')