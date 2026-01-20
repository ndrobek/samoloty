from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import AirplaneModel, PlushToy, OtherGadget
from .serializers import AirplaneModelSerializer, PlushToySerializer, OtherGadgetSerializer


class AirplaneModelListCreateView(generics.ListCreateAPIView):
    queryset = AirplaneModel.objects.all()
    serializer_class = AirplaneModelSerializer


class AirplaneModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AirplaneModel.objects.all()
    serializer_class = AirplaneModelSerializer




class LowStockAirplaneModelsView(APIView):
    def get(self, request):
        low_stock = AirplaneModel.objects.filter(stock__lt=5)
        serializer = AirplaneModelSerializer(low_stock, many=True)
        return Response(serializer.data)


class AirplaneModelsStartingWithView(APIView):
    def get(self, request, letter):
        models = AirplaneModel.objects.filter(
            name__istartswith=letter
        )
        serializer = AirplaneModelSerializer(models, many=True)
        return Response(serializer.data)
