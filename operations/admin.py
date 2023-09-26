from django.contrib import admin
from .models import (
    ProductionMachine, 
    ProductionOrder, 
    ProductionItem,
    ProductionOrderDetails, 
    DispatchOrder, 
    DispatchItem,
    DispatchOrderDetails
)

admin.site.register(ProductionMachine)
admin.site.register(ProductionOrder)
admin.site.register(ProductionItem)
admin.site.register(ProductionOrderDetails)
admin.site.register(DispatchOrder)
admin.site.register(DispatchItem)
admin.site.register(DispatchOrderDetails)