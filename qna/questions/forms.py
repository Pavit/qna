from models import *
from django.forms import ModelForm
from django import forms


class QuestionForm(ModelForm):
	question= forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'What do you want to ask?'}))

	class Meta:
		model = Question
		fields = ("question",)


class AnswerForm(ModelForm):
	answer = forms.CharField(label = "", widget = forms.TextInput(attrs={'placeholder': "What kind of answer do you want?"}))

	class Meta:
		model = Answer
		fields = ("answer",)

