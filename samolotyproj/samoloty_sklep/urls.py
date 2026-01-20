from django.urls import path
from .views import AirplaneModelListCreateView, AirplaneModelDetailView, LowStockAirplaneModelsView, AirplaneModelsStartingWithView

urlpatterns = [
    path('airplanes/', AirplaneModelListCreateView.as_view()),
    path('airplanes/<int:pk>/', AirplaneModelDetailView.as_view()),
    path('airplanes/low-stock/', LowStockAirplaneModelsView.as_view()),
    path('airplanes/starts-with/<str:letter>/', AirplaneModelsStartingWithView.as_view()),
]