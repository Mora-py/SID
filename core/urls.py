from django.urls import path
from .views import LoginView, DashboardView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', LoginView.as_view(), name='root'),
]