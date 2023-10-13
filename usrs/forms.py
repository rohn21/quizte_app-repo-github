from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.db import transaction
from .models import User,Student,Teacher

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField()
    # phone_number = forms.CharField(required=True)
    school_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user)
        student.school_name=self.cleaned_data.get('school_name')
        student.save()
        return user

class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField()
    subject_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
        # icon = {'username': 'user1', 'email': 'email1',}

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.is_staff = True
        user.email = self.cleaned_data.get('email')
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.subject_name=self.cleaned_data.get('subject_name')
        teacher.save()
        return user

class LoginForm(AuthenticationForm):
    # email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput) 
