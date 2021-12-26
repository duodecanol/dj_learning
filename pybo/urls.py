from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.IndexView.as_view()),
    path('<int:question_id>/', views.detail, name='detail'),
]