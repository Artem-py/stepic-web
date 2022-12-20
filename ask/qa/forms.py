from django import forms
from django.contrib.auth.models import User

from .models import Question, Answer


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {'text': forms.Textarea}


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'question']


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        