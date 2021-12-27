from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic

from .forms import QuestionForm, AnswerForm
from .models import Question


def index(request: HttpRequest) -> HttpResponse:
    """Print pybo list
    """
    # input parameter
    page = request.GET.get('page', '1') # Page
    question_list = Question.objects.order_by('-create_date')
    # paging
    paginator = Paginator(question_list, 10) # 10 articles per page
    page_obj = paginator.get_page(page)

    context = { 'question_list': page_obj}
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
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # author attr
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = { 'question': question, 'form': form }
    return render(request, 'pybo/question_detail.html', context)


def question_create(request: HttpRequest) -> HttpResponse:
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user # author attr
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else: # if method is  GET
        form = QuestionForm()
    context = { 'form': form }
    return render(request, 'pybo/question_form.html', context)