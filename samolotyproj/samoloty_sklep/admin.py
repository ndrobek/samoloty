
from django.contrib import admin

from .models import Clothing, AirplaneModel, PlushToy, LuggageTag, Order

admin.site.register(Clothing)
admin.site.register(AirplaneModel)
admin.site.register(PlushToy)
admin.site.register(LuggageTag)
admin.site.register(Order)