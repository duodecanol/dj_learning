from django.urls import path

from pybo import views

urlpatterns = [
    # path('', views.index),
    path('', views.IndexView.as_view()),
    path('<int:question_id>/', views.detail),
]