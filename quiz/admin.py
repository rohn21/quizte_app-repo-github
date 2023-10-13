from django.contrib import admin
from quiz.models import Subject,Quiz,Question,Answer, TakenQuiz


class SubjectAdmin(admin.ModelAdmin):
  list_display = ("id", "name",)

class QuizAdmin(admin.ModelAdmin):
  list_display = ("id", "subject", "name",)

class QuestionAdmin(admin.ModelAdmin):
  list_display = ("id", "quiz","text",)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Quiz, QuizAdmin)

admin.site.register(TakenQuiz)
