from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import CreateView, RedirectView, TemplateView, ListView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormView
from quiz.forms import AddSubject, AddQuiz, AddQuestion, QuestionForm, AnswerFormSet,TakeQuizForm
from quiz.models import Subject, Question, Quiz, Answer, TakenQuiz
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from usrs.decorators import student_required, teacher_required

# Create your views here.
###________________ SUBJECT_RELATED_VIEWS ___________________###

@method_decorator(teacher_required, name='dispatch')
class AddSubject(LoginRequiredMixin, FormView):
    form_class = AddSubject 
    template_name = "quiz/add_subject.html"
    success_url = reverse_lazy('quiz:add-sub')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
@method_decorator(teacher_required, name='dispatch')
class SubjectList(LoginRequiredMixin, ListView):
    model = Subject
    template_name = "quiz/subject_list.html"

@method_decorator(teacher_required, name='dispatch')   
class SubjectUpdate(LoginRequiredMixin, UpdateView):
    model = Subject
    fields = ['name',]
    template_name = "quiz/add_subject.html"
    success_url = reverse_lazy('quiz:sub-list')

@method_decorator(teacher_required, name='dispatch')
class SubjectDelete(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('quiz:sub-list')

###________________ QUIZ_RELATED_VIEWS ___________________###

@method_decorator(teacher_required, name='dispatch')
class AddQuiz(LoginRequiredMixin, FormView):
    form_class = AddQuiz 
    template_name = "quiz/add_quiz.html"
    success_url = reverse_lazy('quiz:add-quiz')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
@method_decorator(teacher_required, name='dispatch')
class QuizTable(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = "quiz/quiz_list.html"
    
@method_decorator(teacher_required, name='dispatch')
class QuizUpdate(LoginRequiredMixin, UpdateView):
    model = Quiz
    fields = ['subject', 'name',]
    template_name = "quiz/add_quiz.html"
    success_url = reverse_lazy('quiz:quiz-list')

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     return kwargs

@method_decorator(teacher_required, name='dispatch')
class QuizDelete(LoginRequiredMixin, DeleteView):
    model = Quiz
    success_url = reverse_lazy('quiz:quiz-list')

###________________ CREATE_QUIZ_RELATED_VIEWS ___________________###

@method_decorator(teacher_required, name='dispatch')
class QuestionList(LoginRequiredMixin, ListView):
    model = Question
    template_name = "quiz/question_list.html"

@method_decorator(teacher_required, name='dispatch')
class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('quiz:question-list')

@method_decorator(teacher_required, name='dispatch')
class AnswerUpdate(LoginRequiredMixin, UpdateView):
    model = Answer
    fields = ['quiz', 'text', 'marks',]
    template_name = "quiz/add_answer.html"
    success_url = reverse_lazy('quiz:answer-list')

@method_decorator(teacher_required, name='dispatch')
class AnswerDelete(LoginRequiredMixin, DeleteView):
    model = Answer
    success_url = reverse_lazy('quiz:answer-list')

@method_decorator(teacher_required, name='dispatch')
class QuesAnsFormView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "quiz/create_quiz.html"
    success_url = reverse_lazy('quiz:question-list')

    def get_context_data(self, **kwargs):
        context = super(QuesAnsFormView, self).get_context_data(**kwargs)
        if self.request.POST:  
            context['answer_set'] = AnswerFormSet(self.request.POST)
        else:
            context['answer_set'] = AnswerFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data(form=form)   
        answer_set = context['answer_set']
        with transaction.atomic():
            self.object = form.save()
        if answer_set.is_valid():
            answer_set.instance = self.object
            answer_set.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(QuesAnsFormView, self).form_invalid(form)
    
    def get_success_url(self):
        return reverse('quiz:question-list')
    
@method_decorator(teacher_required, name='dispatch')
class QuesAnsUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "quiz/create_quiz.html"
    success_url = reverse_lazy('quiz:question-list')

    def get_context_data(self, **kwargs):
        context = super(QuesAnsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:  
            context['answer_set'] = AnswerFormSet(self.request.POST, instance=self.object)
            context['answer_set'].full_clean()
        else:
            context['answer_set'] = AnswerFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data(form=form)   
        answer_set = context['answer_set']
        with transaction.atomic():
            self.object = form.save()
        if answer_set.is_valid():
            answer_set.instance = self.object
            answer_set.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(QuesAnsUpdateView, self).form_invalid(form)
    
    def get_success_url(self):
        return reverse('quiz:question-list')

# class AttendQuiz(FormView):
#     template_name = "attend_quiz/attend_quiz.html"
#     form_class = TakeQuizForm

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         quiz = Quiz.objects.get(pk=self.kwargs['pk'])
#         questions = quiz.questions.all()
#         current_question_index = int(self.request.GET.get('question_index', 0))
#         current_question = questions[current_question_index]
#         kwargs['question'] = current_question
#         return kwargs

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         quiz = Quiz.objects.get(pk=self.kwargs['pk'])
#         questions = quiz.questions.all()
#         current_question_index = int(self.request.GET.get('question_index', 0))
#         current_question_number = current_question_index + 1
#         context['current_question_index'] = current_question_number
#         context['total_questions'] = questions.count()
#         return context

#     def form_valid(self, form):
#         quiz = Quiz.objects.get(pk=self.kwargs['pk'])
#         questions = quiz.questions.all()
#         # answers = Answer.objects.filter(question)
#         current_question_index = int(self.request.GET.get('question_index', 0))
#         current_question = questions[current_question_index]
#         next_question_index = current_question_index + 1
#         # Process the user's response to the current question
#         option = form.cleaned_data['option']
#         print("➡ option :", option.is_correct)
#         # answer = Answer.objects.get(pk=answer_pk)
#         if option.is_correct :
#             # Increment the number of correct answers
#             correct_answers = self.request.session.get('correct_answers', 0)
#             correct_answers += 1
#             self.request.session['correct_answers'] = correct_answers
#             total_marks = self.request.session.get('total_marks', 0)
#             print("➡ total_marks :", total_marks)
#             total_marks += current_question.marks
#             self.request.session['total_marks'] = total_marks

#         if next_question_index >= questions.count():
#             # Quiz is finished, calculate the score and redirect to results page
#             max_marks = questions.aggregate(Sum('marks'))['marks__sum']
#             print("➡ max_marks :", max_marks)
#             total_marks = self.request.session.get('total_marks', 0)
#             print("➡ total_marks :", total_marks)
#             score = round((total_marks / max_marks) * 100)
#             correct_answers = self.request.session.get('correct_answers', 0)
#             TakenQuiz.objects.create(user=self.request.user, quiz=quiz ,answer_id=option.pk, score=score)
#             # return redirect('quiz:result')
#             return HttpResponseRedirect(reverse('quiz:result', args=[quiz.pk]))
#         else:
#             # Display next question
#             return redirect(f'{self.request.path}?question_index={next_question_index}')

@method_decorator(student_required, name='dispatch')
class TakeQuiz(LoginRequiredMixin, FormView):
    template_name = "attend_quiz/attend_quiz.html"
    form_class = TakeQuizForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        questions = quiz.questions.all()
        current_question_index = int(self.request.GET.get('question_index', 0))
        current_question = questions[current_question_index]
        kwargs['question'] = current_question
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        questions = quiz.questions.all()
        current_question_index = int(self.request.GET.get('question_index', 0))
        current_question_number = current_question_index + 1
        context['current_question_index'] = current_question_number
        context['total_questions'] = questions.count()
        return context

    def form_valid(self, form):
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        questions = quiz.questions.all()
        current_question_index = int(self.request.GET.get('question_index', 0))
        current_question = questions[current_question_index]
        next_question_index = current_question_index + 1
        option = form.cleaned_data['option']

        # Initialize session variables if they don't exist
        if 'correct_answers' not in self.request.session:
            self.request.session['correct_answers'] = 0
        if 'total_marks' not in self.request.session:
            self.request.session['total_marks'] = 0

        # Process the user's response to the current question
        if option.is_correct:
            self.request.session['correct_answers'] += 1
            self.request.session['total_marks'] += current_question.marks
        
        # Mark the session as modified to make sure it gets saved
        self.request.session.modified = True

        if next_question_index >= questions.count():
        # Quiz is finished, calculate the score and redirect to results page
            max_marks = (questions.aggregate(Sum('marks'))['marks__sum'])
            score = round((self.request.session['total_marks'] / max_marks) * 100)
            score = (self.request.session['total_marks'])*100
            TakenQuiz.objects.create(user=self.request.user, quiz=quiz ,answer_id=option.pk, score=score)

            return HttpResponseRedirect(reverse('quiz:result', args=[quiz.pk]))
        else:
            # Display next question
            return redirect(f'{self.request.path}?question_index={next_question_index}')

###___________________________ ATTENDED-QUIZ_RELATED_VIEWS ________________________###

@method_decorator(student_required, name='dispatch')
class QuizList(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = "attend_quiz/quizzes.html"
        
@method_decorator(student_required, name='dispatch')
class QuizResultsView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'attend_quiz/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taken_quiz = TakenQuiz.objects.filter(user=self.request.user).last()
        max_marks = Question.objects.filter(quiz=taken_quiz.quiz).aggregate(Sum('marks'))['marks__sum']
        quiz = self.get_object()
        context['attempts'] =  TakenQuiz.objects.filter(user=self.request.user, quiz=quiz).count()
        context['answers']= self.request.session.get('correct_answers', 0)
        context['max_marks'] = (max_marks *100)
        context['taken_quiz'] = taken_quiz

        # to clear session variables
        del self.request.session['correct_answers']
        del self.request.session['total_marks']
        return context

