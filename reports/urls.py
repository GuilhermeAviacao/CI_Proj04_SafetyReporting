from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('board/', views.board, name='board'),
    path('create/', views.create_report, name='create_report'),
]
