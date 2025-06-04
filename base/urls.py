from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.ExpenTrackListView, name='home'),
    path('expense/<int:pk>/', views.ExpenseTrackerDetailView.as_view(), name='expense_detail'),
    path('delete/<int:pk>/', views.ExpenseTrackerDeleteView.as_view(), name='delete'),
]
