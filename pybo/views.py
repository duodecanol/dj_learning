from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Question


def index(request: HttpRequest) -> HttpResponse:
    """Print pybo list
    """
    question_list = Question.objects.order_by('-create_date')
    context = { 'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    """Print pybo detail
    """
    question = get_object_or_404(Question, pk=question_id)
    context = { 'question': question }
    return render(request, 'pybo/question_detail.html', context)

class IndexView(generic.ListView):
    def get_queryset(self):
        return Question.objects.order_by('-create_date')