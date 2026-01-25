
from django.contrib import admin
from .models import Clothing, AirplaneModel, PlushToy, LuggageTag, Order, ClothingMaterial


admin.site.register(AirplaneModel)
admin.site.register(PlushToy)
admin.site.register(LuggageTag)
admin.site.register(Order)
admin.site.register(ClothingMaterial)
@admin.register(Clothing)
class ClothingAdmin(admin.ModelAdmin):
    filter_horizontal = ("material")