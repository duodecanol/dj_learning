from django.urls import path

from pybo import views

urlpatterns = [
    path('', views.index),
    path('<int:question_id>/', views.detail),
]