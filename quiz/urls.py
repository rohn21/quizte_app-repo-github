from django.urls import path, include
from quiz.views import (AddSubject, AddQuiz, QuesAnsFormView
                         ,SubjectList, QuizTable, QuestionList
                         ,SubjectUpdate,QuizUpdate,QuesAnsUpdateView 
                         ,SubjectDelete, QuizDelete, QuestionDelete, TakeQuiz
                        , QuizList, QuizResultsView)
from django.views.generic import TemplateView

app_name = 'quiz'

urlpatterns=[
    #subject
    path('add-sub/', AddSubject.as_view(), name='add-sub'),
    path('sub/', SubjectList.as_view(), name='sub-list'),
    path('sub/update/<pk>', SubjectUpdate.as_view(), name='sub-update'),
    path('sub/delete/<pk>', SubjectDelete.as_view(), name='sub-delete'),

    #quiz
    path('add-quiz/', AddQuiz.as_view(), name='add-quiz'),
    path('quizzes/', QuizTable.as_view(), name='quizzes'),
    path('quiz/update/<pk>', QuizUpdate.as_view(), name='quiz-update'),
    path('quiz/delete/<pk>', QuizDelete.as_view(), name='quiz-delete'),

    #create_quiz
    path('create-quiz/', QuesAnsFormView.as_view(), name='create-quiz'),
    path('question/delete/<pk>', QuestionDelete.as_view(), name='question-delete'),
    path('quesans/update/<pk>', QuesAnsUpdateView.as_view(), name='quesans-update'),
    path('qustions/', QuestionList.as_view(), name='question-list'),

    #takequiz
    path('quiz-list/', QuizList.as_view(), name='quiz-list'),
    path('attend/<pk>/', TakeQuiz.as_view(), name='attend-quiz'),
    path('result/<pk>/', QuizResultsView.as_view(), name='result'),

]