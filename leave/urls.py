from django.urls import path
from . import views

urlpatterns = [
    path('', views.leave_list, name='leave_list'),
    path('new/', views.leave_create, name='leave_create'),
    path('edit/<int:pk>/', views.leave_edit, name='leave_edit'),
    path('delete/<int:pk>/', views.leave_delete, name='leave_delete'),
    path('approve/<int:pk>/', views.leave_approve, name='leave_approve'),
    path('reject/<int:pk>/', views.leave_reject, name='leave_reject'),
    path('override_delete/<int:pk>/', views.leave_override_delete, name='leave_override_delete'),
]
