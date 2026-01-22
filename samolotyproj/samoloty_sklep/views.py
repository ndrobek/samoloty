from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import AirplaneModel, PlushToy, LuggageTag, Order
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from .serializers import AirplaneModelSerializer, PlushToySerializer, LuggageTagSerializer, OrderSerializer, RegisterSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth
from django.db.models import Count



class AirplaneModelListCreateView(generics.ListCreateAPIView):
    queryset = AirplaneModel.objects.all()
    serializer_class = AirplaneModelSerializer
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]


class AirplaneModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AirplaneModel.objects.all()
    serializer_class = AirplaneModelSerializer
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]




class LowStockAirplaneModelsView(APIView):
    def get(self, request):
        low_stock = AirplaneModel.objects.filter(stock__lt=5)
        serializer = AirplaneModelSerializer(low_stock, many=True)
        return Response(serializer.data)


class AirplaneModelsStartingWithView(APIView):
    def get(self, request, letter):
        models = AirplaneModel.objects.filter(name__istartswith=letter)
        serializer = AirplaneModelSerializer(models, many=True)
        return Response(serializer.data)


class OrderListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class OrderDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def order_delete(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=404)

    if order.user != request.user and not request.user.is_staff:
        return Response(
            {"detail": "Nie masz uprawnień do usunięcia tego zamówienia!!"},
            status=403
        )

    order.delete()
    return Response(status=204)



class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        password2 = request.data.get('password2')

        if not username or not password:
            return Response(
                {"error": "Wymagane są nazwa użytkownika oraz hasło."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != password2:
            return Response(
                {"error": "Hasło jest błędne."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Taki użytkownik już istnieje."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)
        return Response(
            {"message": "Utworzono użytkownika :)."},
            status=status.HTTP_201_CREATED
        )


class LuggageTagListCreateView(ListCreateAPIView):
    queryset = LuggageTag.objects.all()
    serializer_class = LuggageTagSerializer
    permission_classes = [IsAuthenticated]


class LuggageTagDetailView(RetrieveUpdateDestroyAPIView):
    queryset = LuggageTag.objects.all()
    serializer_class = LuggageTagSerializer
    permission_classes = [IsAuthenticated]


class PlushToyListCreateView(ListCreateAPIView):
    queryset = PlushToy.objects.all()
    serializer_class = PlushToySerializer
    permission_classes = [IsAuthenticated]


class PlushToyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = PlushToy.objects.all()
    serializer_class = PlushToySerializer
    permission_classes = [IsAuthenticated]





# Lista zamówień danego użytkownika (aktualnie zalogowanego)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# Zestawienie miesięczne

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_orders_summary(request):
    data = (
        Order.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    return Response(data)