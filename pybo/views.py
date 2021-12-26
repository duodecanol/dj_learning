from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
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


def answer_create(request: HttpRequest, question_id: int) -> HttpResponse:
    """
    pybo 답변 등록
    """
    print("wow")
    question = get_object_or_404(Question, pk=question_id)
    # foreign key 로 연결되어있기 때문에 다음과 같이 new Answer 생성 가능.
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # Alternatively, direct creation through Answer class
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()
    return redirect('pybo:detail', question_id=question.id)