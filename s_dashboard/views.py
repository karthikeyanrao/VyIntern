from django.shortcuts import render,HttpResponse
from django.shortcuts import render
from django.utils.timezone import now,make_aware
from login.models import LoginStudent  # Import student model
from t_dashboard.models import Test 
from django.utils.timezone import now
from datetime import datetime # Import Test model
import pytz

def student_dashboard(request):
    student_username = request.session.get("s_username")  # Get the logged-in student's username
    if not student_username:
        return HttpResponse("no student profile found")
    # Get the student from LoginStudent model
    try:
        student = LoginStudent.objects.get(username=student_username)
    except LoginStudent.DoesNotExist:
        return HttpResponse("not found")
    print(student)
    upcoming_tests = Test.objects.filter(
        department=student.dept, 
        year_of_study=student.year,
        date_of_test__gte=now().date()
    ).order_by('date_of_test', 'start_time')

    current_datetime = now()  # Timezone-aware current datetime

    for test in upcoming_tests:
        test.show_join_button = False  # Default value
        if test.date_of_test == current_datetime.date():
            test_datetime = datetime.combine(current_datetime.date(), test.start_time)  # Naive datetime
            test_datetime = make_aware(test_datetime, timezone=pytz.UTC)  # Convert to aware
            print("Test Start Time (Aware):", test_datetime)  # Debugging

            time_diff = (test_datetime - current_datetime).total_seconds()
            print(f"Time Difference for {test.subject}: {time_diff} seconds")  # Debugging

            test.show_join_button = 0 <= time_diff <= 300

    return render(request, "student_dashboard.html", {"upcoming_tests": upcoming_tests})

# Create your views here.
