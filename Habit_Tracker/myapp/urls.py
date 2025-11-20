from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create/", views.create_habit, name="create_habit"),
    path("toggle/<int:habit_id>/", views.toggle_done, name="toggle_done"),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
