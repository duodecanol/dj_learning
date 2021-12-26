from django import forms
from pybo.models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question # model to use
        fields = ['subject', 'content'] # model attributes for using in QuestionForm