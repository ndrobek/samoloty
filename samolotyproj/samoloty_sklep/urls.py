from django.urls import path
from .views import AirplaneModelListCreateView, AirplaneModelDetailView, LowStockAirplaneModelsView, AirplaneModelsStartingWithView, OrderListCreateView, OrderDetailView, RegisterUserView, monthly_orders_summary, my_orders

urlpatterns = [
    path('airplanes/', AirplaneModelListCreateView.as_view()),
    path('airplanes/<int:pk>/', AirplaneModelDetailView.as_view()),
    path('airplanes/low-stock/', LowStockAirplaneModelsView.as_view()),
    path('airplanes/starts-with/<str:letter>/', AirplaneModelsStartingWithView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
    path('orders/my/', my_orders),
    path('orders/monthly-summary/', monthly_orders_summary),
]