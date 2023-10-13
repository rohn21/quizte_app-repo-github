from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, RedirectView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from .forms import StudentSignUpForm, TeacherSignUpForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout,authenticate
from usrs.models import User, Student
from django.db.models import Sum
from  quiz.models import Question,TakenQuiz,Quiz,Subject
from django.utils.decorators import method_decorator
from usrs.decorators import student_required, teacher_required

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

         # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get_success_url(self):
        if self.request.user.is_student:
            return reverse_lazy('usrs:student')
        elif self.request.user.is_teacher:
            return reverse_lazy('usrs:teacher')
        else:
            return reverse_lazy('usrs:home')

class StudentRegister(SuccessMessageMixin, CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/student_register.html'
    success_url = reverse_lazy('usrs:login')
    success_message = 'Congratulation, Registration successful | Please login to continue !!!!'

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect(self.success_url)

class TeacherRegister(SuccessMessageMixin, CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/teacher_register.html'
    success_url = reverse_lazy('usrs:login')
    success_message = 'Congratulation, Registration successful | Please login to continue !!!!'

    # for directly redirect to userpage after user_registration
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('usrs:teacher')

class LogoutView(RedirectView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('usrs:login'))

@method_decorator(student_required, name='dispatch')
class StudentHome(LoginRequiredMixin, TemplateView):
    model = TakenQuiz
    template_name = "user/student_home.html"
    login_url = 'usrs:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.select_related('user').all()
        for student in students:
            student.unique_quiz = TakenQuiz.objects.filter(user=student.user).count()
        context['attempts'] =  students
        user = self.request.user
        context['taken_quizzes'] = TakenQuiz.objects.filter(user=user)
        context['answers']= self.request.session.get('correct_answers', 0)
        return context
    
@method_decorator(teacher_required, name='dispatch')
class TeacherHome(LoginRequiredMixin, TemplateView):
    model = Quiz
    template_name = "user/teacher_home.html"
    login_url = 'usrs:login'
    # redirect_field_name = 'usrs:login'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['sub'] = Subject.objects.values('name', ).distinct().count()
        context['quiz'] = Quiz.objects.values('name', ).count()
        student = Student.objects.all()
        context['users'] = student.values('user').count()
        students = Student.objects.select_related('user').all()
        for student in students:
            student.unique_quiz_count = TakenQuiz.objects.filter(user=student.user).values('quiz').distinct().count()
            quiz_score = TakenQuiz.objects.filter(user=student.user).order_by('-score').first()
            taken_quiz = TakenQuiz.objects.filter(user=student.user).order_by('-created_at').first()
            student.quiz_date = taken_quiz.created_at if taken_quiz else None
            student.highest_score = quiz_score.score if quiz_score else None
        context['quizzes'] = students
        return context

class UserProfile(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "user/profile.html"