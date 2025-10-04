from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('board/', views.board, name='board'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('report/<int:pk>/update-status/', views.update_investigation_status, name='update_investigation_status'),
    path('create/', views.create_report, name='create_report'),
]
