from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from common.forms import UserForm


def signup(request: HttpRequest) -> HttpResponse:
    """
    Account creation
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # User Authentication
            login(request, user) # Log in
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', { 'form': form })