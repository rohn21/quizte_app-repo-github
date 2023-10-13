from django.conf import settings
from django.db import models
User = settings.AUTH_USER_MODEL
# from usrs.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Subject(BaseModel):
    name = models.CharField(max_length=255, unique=True) #added unique constraint to avoid duplication

    def __str__(self):
        return self.name

class Quiz(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "quizzes"

class Question(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.text

class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    option = models.CharField(max_length=255,)
    is_correct = models.BooleanField(default = False)

    def __str__(self):
        return self.option
    
class TakenQuiz(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='takenquiz')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='takenquiz')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='takenquiz')
    score = models.IntegerField()