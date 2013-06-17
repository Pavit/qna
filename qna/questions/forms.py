from models import *
from django.forms import ModelForm
from django import forms

stat_choices = (
('age', 'Age'),
('gender', 'Gender'),
)

class QuestionForm(ModelForm):
	question= forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'What do you want to ask?'}))

	class Meta:
		model = Question
		fields = ("question",)


class AnswerForm(ModelForm):
	answer = forms.CharField(label = "", widget = forms.TextInput(attrs={'placeholder': "What kind of answer do you want?"}))

	class Meta:
		model = Answer
		exclude = ("question", "selected_by", "votes",)


class StatForm(forms.Form):
	stat = forms.ChoiceField(choices = stat_choices, widget=forms.Select(attrs={'onchange':'loadStat(this)'}))

	def __init__(self, *args, **kwargs):
		super(StatForm, self).__init__(*args, **kwargs)
		self.fields['stat'].choices.insert(0, ('','---------' ) )

