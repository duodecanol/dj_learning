from django import forms
from pybo.models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question # model to use
        fields = ['subject', 'content'] # model attributes for using in QuestionForm
        # widgets = {
        #     'subject': forms.TextInput(attrs={ 'class': 'form-control' }),
        #     'content': forms.Textarea(attrs={ 'class': 'form-control', 'rows': 10 }),
        # }
        labels = {
            'subject': '제목',
            'content': '내용',
        }