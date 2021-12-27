from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer


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

@login_required(login_url='common:login')
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

@login_required(login_url='common:login')
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

@login_required(login_url='common:login')
def question_modify(request: HttpRequest, question_id: int) -> HttpResponse:
    """
    pybo 질문 수정
    """
    question =get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = { 'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request: HttpRequest, question_id: int) -> HttpResponse:
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_modify(request: HttpRequest, answer_id: int) -> HttpResponse:
    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return  redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = { 'answer': answer, 'form': form }
    return render(request, 'pybo/answer_form.html', context)