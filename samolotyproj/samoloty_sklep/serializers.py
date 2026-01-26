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
                "Price has to be greater than 0!"
            )
        return value

    def validate(self, data):
        scale = data.get('scale')
        material = data.get('material')

        if scale == '1:400' and material == 'PC':
            raise serializers.ValidationError(
                "1:400 scaled models cannot be made of plastic."
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
                "The price of a plush has to be at least 10."
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
                "The design has to be in UPPERCASE LETTERS"
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']

