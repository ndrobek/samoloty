from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AirplaneModel, PlushToy, LuggageTag, Order


class AirplaneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneModel
        fields = '__all__'
        read_only_fields = ['id']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cena musi być większa od 0."
            )
        return value

    def validate(self, data):
        scale = data.get('scale')
        material = data.get('material')

        if scale == '1:400' and material == 'PC':
            raise serializers.ValidationError(
                "Modele 1:400 nie mogą być wykonane z plastiku."
            )
        return data



class PlushToySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlushToy
        fields = '__all__'
        read_only_fields = ['id']

    def validate_price(self, value):
        if value < 10:
            raise serializers.ValidationError(
                "Cena pluszaka ma wynosić conajmniej 10 zł."
            )
        return value



class LuggageTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = LuggageTag
        fields = '__all__'
        read_only_fields = ['id']

    def validate_design(self, value):
        if value != value.upper():
            raise serializers.ValidationError(
                "Tekst na zawieszce musi być zapisany wielkimi literami."
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']

