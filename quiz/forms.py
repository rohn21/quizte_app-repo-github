from django import forms
from django.forms import ModelForm, formset_factory, modelformset_factory
from django.db import transaction
from quiz.models import Subject, Quiz, Question, Answer
from django.forms.models import inlineformset_factory

class AddSubject(forms.ModelForm):

    ### only if you want to render form manually
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs['class'] = 'form-control'
    #     self.fields['name'].widget.attrs['placeholder'] = 'form-control'
    ###
        
    class Meta:
        model = Subject
        fields = ('name',)

class AddQuiz(forms.ModelForm):
     
    class Meta:
        model = Quiz
        fields = ('subject', 'name',)

class AddQuestion(forms.ModelForm):
     
    class Meta:
        model = Question
        fields = ('quiz', 'text', 'marks')

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ('quiz', 'text')
        widgets = { 
            'quiz': forms.Select(attrs={'class': ' form-group form-control'}),
            'text': forms.Textarea(attrs={'class': ' form-group form-control', 'placeholder':'Enter the question'}),
        } 
        exclude = ()


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        # fields = ['question']
        exclude = ()

AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm,widgets = { 
            'option': forms.TextInput(attrs={'class': ' orm-group form-control', }),
            'is_correct': forms.CheckboxInput(attrs={'class': 'ml-4'}),
        }, extra=4, max_num=5 ,can_delete=False)



class TakeQuizForm(forms.ModelForm):
    option = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(attrs={'class': 'mt-2 ml-4 mb-2'}),
        empty_label=None,
        required=True
    )
    
    question_text = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Answer
        fields = ('option','question_text')
        

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['option'].queryset = question.answers.all()
        self.fields['question_text'].initial = question.text