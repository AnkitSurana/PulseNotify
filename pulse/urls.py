from django.urls import path
from .views import RegisterView, LoginView, AlertListCreateView, AlertDeleteView, get_flight_price, AdminSummaryView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('alerts/', AlertListCreateView.as_view(), name='alerts'),
    path('alerts/<int:id>/', AlertDeleteView.as_view(), name='alert-detail'),
    path('flights/price/', get_flight_price, name='flight-price'),
    path('admin/summary/', AdminSummaryView.as_view(), name='admin-summary'),
]
