from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from .models import Test, Question, TestEnrollment
from django.contrib import messages
from login.models import LoginStudent
from django.db.models import Q

def t_dashboard(request):
    username=request.session.get('t_username')
    staffid=request.session.get('t_staffid')
    emailid=request.session.get('t_emailid')
    dept=request.session.get('t_dept')
    return render(request,'teacher_dashboard.html',{'username':username,'staffid':staffid,'emailid':emailid,'dept':dept})

def create_test(request):
    if request.method == "POST":
        subject_name = request.POST["subject_name"]
        subject_code = request.POST["subject_code"]
        date_of_test = request.POST["date_of_test"]
        start_time = request.POST["start_time"]
        duration = request.POST["duration"]
        department = request.POST["department"]
        year = request.POST["year"]

        # Create a new Test entry
        new_test=Test.objects.create(
            subject=subject_name,
            subject_code=subject_code,
            date_of_test=date_of_test,
            start_time=start_time,
            duration=duration,
            department=department,
            year_of_study=year
        )
        print(new_test.test_id)
        request.session['testid']= new_test.test_id

        return redirect("add_question")  # Redirect to test list page

    return render(request, "c_test.html")

def evaluate_test(request):
    return HttpResponse("this is evaluate test page")

def class_group(request):
   return HttpResponse("this is class_group page")

def test_details(request):
    if 't_username' not in request.session:
        messages.error(request, "Please login as a teacher first")
        return redirect('teacher_admin')

    # Get all tests created by the teacher
    tests = Test.objects.all().order_by('-date_of_test', '-start_time')
    
    # Get enrollment counts for each test
    for test in tests:
        test.enrollment_count = TestEnrollment.objects.filter(test=test).count()
    
    return render(request, 'test_details.html', {
        'tests': tests,
        'username': request.session.get('t_username'),
        'staffid': request.session.get('t_staffid'),
        'emailid': request.session.get('t_emailid'),
        'dept': request.session.get('t_dept')
    })

def add_question(request):
    if request.GET.get("test_id"):
        testid = request.GET.get("test_id")
    else:
        testid=request.session.get('testid')
    num_questions = Question.objects.filter(test_id=testid).count()+1
    if request.method == "POST":
        question_text = request.POST.get("question_text")
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")
        correct_option = request.POST.get("correct_option")
        points = request.POST.get("points")
        
        # Save question to database
        Question.objects.create(
            test_id=testid,
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            points=points
        )
        # If "Finish" button is clicked, redirect to test details pag
        if "finish" in request.POST:
            return redirect("test_questions_list")
        # If "Next Question" is clicked, stay on the form
        return redirect("add_question")

    return render(request, "add_questions.html", {"test":testid,'question_no':num_questions })

def test_questions_list(request):
    testid = request.GET.get("test_id")
    if not testid:
        return redirect("test_details")
    Questions = Question.objects.filter(test_id=testid)
    return render(request, 'test_questions_list.html', {'Questions':Questions,'testid':testid})

def manage_enrollments(request, test_id):
    if 't_username' not in request.session:
        messages.error(request, "Please login as a teacher first")
        return redirect('teacher_admin')

    test = get_object_or_404(Test, test_id=test_id)
    
    # Get all students from the same department and year
    eligible_students = LoginStudent.objects.filter(
        dept=test.department,
        year=test.year_of_study
    )

    # Get currently enrolled students
    enrolled_students = TestEnrollment.objects.filter(test=test).select_related('student')

    if request.method == 'POST':
        action = request.POST.get('action')
        student_username = request.POST.get('student_username')

        if action == 'enroll':
            try:
                student = LoginStudent.objects.get(username=student_username)
                TestEnrollment.objects.create(test=test, student=student)
                messages.success(request, f"Successfully enrolled {student_username}")
            except LoginStudent.DoesNotExist:
                messages.error(request, "Student not found")
            except Exception as e:
                messages.error(request, f"Error enrolling student: {str(e)}")

        elif action == 'unenroll':
            try:
                enrollment = TestEnrollment.objects.get(test=test, student__username=student_username)
                enrollment.delete()
                messages.success(request, f"Successfully unenrolled {student_username}")
            except TestEnrollment.DoesNotExist:
                messages.error(request, "Enrollment not found")

    context = {
        'test': test,
        'eligible_students': eligible_students,
        'enrolled_students': enrolled_students,
        'username': request.session.get('t_username'),
        'staffid': request.session.get('t_staffid'),
        'emailid': request.session.get('t_emailid'),
        'dept': request.session.get('t_dept')
    }
    return render(request, 'manage_enrollments.html', context)

# Create your views here.
