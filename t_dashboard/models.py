from django.db import models
from login.models import LoginStudent

class Test(models.Model):
    test_id = models.AutoField(primary_key=True)  # Unique Test ID
    subject = models.CharField(max_length=255)  # Subject Name
    subject_code = models.CharField(max_length=50)  # Subject Code
    date_of_test = models.DateField()  # Test Date
    start_time = models.TimeField()  # Test Start Time
    duration = models.CharField(max_length=8)  # Test Duration (HH:MM:SS format)
    department = models.CharField(max_length=100)  # Department Name
    year_of_study = models.IntegerField()  # Year of Study (1, 2, 3, etc.)

    def __str__(self):
        return f"{self.subject} ({self.subject_code})"

class Question(models.Model):
    test_id = models.IntegerField()
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=50)  # Stores "option1", "option2", etc.
    points = models.IntegerField()

    def __str__(self):
        return f"Question for Test {self.test_id}"

class TestEnrollment(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(LoginStudent, on_delete=models.CASCADE, related_name='test_enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('not_attempted', 'Not Attempted')
    ], default='enrolled')

    class Meta:
        unique_together = ('test', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.test.subject}"

# Create your models here.
