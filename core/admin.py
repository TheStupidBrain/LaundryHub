from django.contrib import admin
from .models import User, Service, Order, OrderItem

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderItem)
