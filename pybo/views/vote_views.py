from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

@login_required(login_url='common:login')
def vote_question(request: HttpRequest, question_id: int) -> HttpResponse:
    return None