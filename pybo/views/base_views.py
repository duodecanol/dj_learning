from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from ..models import Question


def index(request: HttpRequest) -> HttpResponse:
    """Print pybo list
    """
    # input parameter
    page = request.GET.get('page', '1')  # Page
    kw = request.GET.get('kw', '')  # search keyword
    so = request.GET.get('so', 'recent') # sorting criterion

    # sorting
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    elif so == 'recent':
        question_list = Question.objects.order_by('-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')


    # retrieve
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |              # 질문.제목 검색
            Q(content__icontains=kw) |              # 질문.내용 검색
            Q(author__username__icontains=kw) |     # 질문.글쓴이.username 검색
            Q(answer__author__username__icontains=kw)  # 질문.답변.글쓴이.username 검색
        ).distinct()

    # pagination
    paginator = Paginator(question_list, 10)  # 10 articles per page
    page_obj = paginator.get_page(page)

    context = { 'question_list': page_obj, 'page': page, 'kw': kw, 'so': so }
    return render(request, 'pybo/question_list.html', context)


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    """Print pybo detail
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


class IndexView(generic.ListView):
    def get_queryset(self):
        return Question.objects.order_by('-create_date')
