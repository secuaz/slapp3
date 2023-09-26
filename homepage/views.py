from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from operations.models import DispatchOrder, ProductionOrder


class HomeView(View):
    template_name = "home.html"
    def get(self, request):        
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
        orders = DispatchOrder.objects.order_by('-time')[:3]
        productions = ProductionOrder.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'data'      : data,
            'orders'     : orders,
            'productions' : productions
        }
        return render(request, self.template_name, context)

