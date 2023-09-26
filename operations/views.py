from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    ProductionOrder,
    ProductionMachine,
    ProductionItem,
    ProductionOrderDetails,
    DispatchOrder,
    DispatchItem,
    DispatchOrderDetails,
)
from .forms import (
    SelectMachineForm,
    ProductionItemFormset,
    ProductionDetailsForm,
    MachineForm,
    DispatchForm,
    DispatchItemFormset,
    DispatchDetailsForm,
)
from inventory.models import Stock


# Muestra lista de equipos
class MachineListView(ListView):
    model = ProductionMachine
    template_name = "machine/machine_list.html"
    queryset = ProductionMachine.objects.filter(is_deleted=False)
    paginate_by = 10


# View para crear equipos
class MachineCreateView(SuccessMessageMixin, CreateView):
    model = ProductionMachine
    form_class = MachineForm
    success_url = "/operations/machine"
    success_message = "Equipo creado correctamente"
    template_name = "machine/edit_machine.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nuevo Equipo"
        context["savebtn"] = "Crear Equipo"
        return context


# View para modificar equipos
class MachineUpdateView(SuccessMessageMixin, UpdateView):
    model = ProductionMachine
    form_class = MachineForm
    success_url = "/operations/machine"
    success_message = "Equipo actualizado correctamente"
    template_name = "machine/edit_machine.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Equipo"
        context["savebtn"] = "Guardar Cambios"
        context["delbtn"] = "Eliminar Equipo"
        return context


# View para borrar equipos
class MachineDeleteView(View):
    template_name = "machine/delete_machine.html"
    success_message = "Equipo eliminado correctamente"

    def get(self, request, pk):
        machine = get_object_or_404(ProductionMachine, pk=pk)
        return render(request, self.template_name, {"object": machine})

    def post(self, request, pk):
        machine = get_object_or_404(ProductionMachine, pk=pk)
        machine.is_deleted = True
        machine.save()
        messages.success(request, self.success_message)
        return redirect("machine-list")


# View para visualizar equipos
class MachineView(View):
    def get(self, request, name):
        machineobj = get_object_or_404(ProductionMachine, name=name)
        order_list = ProductionOrder.objects.filter(machine=machineobj)
        page = request.GET.get("page", 1)
        paginator = Paginator(order_list, 10)
        try:
            order = paginator.page(page)
        except PageNotAnInteger:
            order = paginator.page(1)
        except EmptyPage:
            order = paginator.page(paginator.num_pages)
        context = {"machine": machineobj, "orders": order}
        return render(request, "machine/machine.html", context)


# View para listar prducciones
class ProductionView(ListView):
    model = ProductionOrder
    template_name = "production/production_list.html"
    context_object_name = "orders"
    ordering = ["-time"]
    paginate_by = 10


# View para seleccionar equipos en formulario de produccion
class SelectMachineView(View):
    form_class = SelectMachineForm
    template_name = "production/select_machine.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            machineid = request.POST.get("machine")
            machine = get_object_or_404(ProductionMachine, id=machineid)
            return redirect("new-production", machine.pk)
        return render(request, self.template_name, {"form": form})


# View para crear orden de produccion
class ProductionCreateView(View):
    template_name = "production/new_production.html"

    def get(self, request, pk):
        formset = ProductionItemFormset(request.GET or None)
        productionobj = get_object_or_404(ProductionMachine, pk=pk)
        context = {
            "formset": formset,
            "machine": productionobj,
        }
        print(request)
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = ProductionItemFormset(request.POST)
        machineobj = get_object_or_404(ProductionMachine, pk=pk)
        if formset.is_valid():
            orderobj = ProductionOrder(machine=machineobj)
            orderobj.save()
            orderdetailsobj = ProductionOrderDetails(orderno=orderobj)
            orderdetailsobj.save()
            # forloop para guardar los forms individuales com objetos
            for form in formset:
                # Vincula la orden con el item
                orderitem = form.save(commit=False)
                # Vincula el item al objeto
                orderitem.orderno = orderobj
                # Obtiene el producto vinculado
                stock = get_object_or_404(Stock, name=orderitem.stock.name)
                # Actualiza la cantidad
                stock.quantity += orderitem.quantity
                # Guarda la orden y el producto
                stock.save()
                orderitem.save()
            # Guarda los detalles de la orden
            orderdetailsobj.save()
            # Envia el mensaje a la View siguiente
            messages.success(
                request, "El producto producido ha sido registrado correctamente"
            )
            # Redirecciona a la orden creada para visualizar e imprimir
            return redirect("production-order", orderno=orderobj.orderno)
        formset = ProductionItemFormset(request.GET or None)
        context = {"formset": formset, "machine": machineobj}
        return render(request, self.template_name, context)


class ProductionDeleteView(SuccessMessageMixin, DeleteView):
    model = ProductionOrder
    template_name = "production/delete_production.html"
    success_url = "/operations/production"

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = ProductionItem.objects.filter(orderno=self.object.orderno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(self.request, "La produccion ha sido borrada correctamente")
        return super(ProductionDeleteView, self).delete(*args, **kwargs)


# Lista despachos
class DispatchView(ListView):
    model = DispatchOrder
    template_name = "dispatch/dispatch_list.html"
    context_object_name = "orders"
    ordering = ["-time"]
    paginate_by = 10


# Genera orden de despacho
class DispatchCreateView(View):
    template_name = "dispatch/new_dispatch.html"

    def get(self, request):
        form = DispatchForm(request.GET or None)
        formset = DispatchItemFormset(request.GET or None)
        stocks = Stock.objects.filter(is_deleted=False)
        context = {"form": form, "formset": formset, "stocks": stocks}
        return render(request, self.template_name, context)

    def post(self, request):
        form = DispatchForm(request.POST)
        formset = DispatchItemFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            # Guardar Orden
            try:
                orderobj = form.save(commit=False)
                orderobj.save()

            except Exception as exc:
                print("Exception error! ", exc)
                context = {
                    "form": form,
                    "formset": formset,
                }
                return render(request, self.template_name, context)

            try:
                # Crea detalles de la orden
                orderdetailsobj = DispatchOrderDetails(orderno=orderobj)
                orderdetailsobj.save()

            except Exception as exc:
                print("Exception error! ", exc)
                orderobj.delete()
                context = {
                    "form": form,
                    "formset": formset,
                }
                return render(request, self.template_name, context)

            for form in formset:
                orderitem = form.save(commit=False)
                orderitem.orderno = orderobj
                stock = get_object_or_404(Stock, name=orderitem.stock.name)
                stock.quantity -= orderitem.quantity
                stock.save()
                orderitem.save()

            orderdetailsobj.save()
            messages.success(
                request, "Los productos del pedido han sido registrados correctamente"
            )
            return redirect("dispatch-order", orderno=orderobj.orderno)
        form = DispatchForm(request.GET or None)
        formset = DispatchItemFormset(request.GET or None)
        context = {
            "form": form,
            "formset": formset,
        }
        return render(request, self.template_name, context)


class DispatchDeleteView(SuccessMessageMixin, DeleteView):
    model = DispatchOrder
    template_name = "dispatch/delete_dispatch.html"
    success_url = "/operations/dispatch"

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = DispatchItem.objects.filter(orderno=self.object.orderno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(self.request, "Pedido eliminado correctamente")
        return super(DispatchDeleteView, self).delete(*args, **kwargs)


class ProductionOrderView(View):
    model = ProductionOrder
    template_name = "order/production_order.html"
    order_base = "order/order_base.html"

    def get(self, request, orderno):
        context = {
            "order": ProductionOrder.objects.get(orderno=orderno),
            "items": ProductionItem.objects.filter(orderno=orderno),
            "orderdetails": ProductionOrderDetails.objects.get(orderno=orderno),
            "order_base": self.order_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, orderno):
        form = ProductionDetailsForm(request.POST)
        if form.is_valid():
            orderdetailsobj = ProductionOrderDetails.objects.get(orderno=orderno)
            orderdetailsobj.eway = request.POST.get("eway")
            orderdetailsobj.veh = request.POST.get("veh")
            orderdetailsobj.destination = request.POST.get("destination")
            orderdetailsobj.po = request.POST.get("po")
            orderdetailsobj.cgst = request.POST.get("cgst")
            orderdetailsobj.sgst = request.POST.get("sgst")
            orderdetailsobj.igst = request.POST.get("igst")
            orderdetailsobj.cess = request.POST.get("cess")
            orderdetailsobj.tcs = request.POST.get("tcs")
            orderdetailsobj.total = request.POST.get("total")
            orderdetailsobj.save()
            messages.success(
                request, "Los detalles de produccion han sido actualizado correctamente"
            )
        context = {
            "order": ProductionOrder.objects.get(orderno=orderno),
            "items": ProductionItem.objects.filter(orderno=orderno),
            "orderdetails": ProductionOrderDetails.objects.get(orderno=orderno),
            "order_base": self.order_base,
        }
        return render(request, self.template_name, context)


class DispatchOrderView(View):
    model = DispatchOrder
    template_name = "order/dispatch_order.html"
    order_base = "order/order_base.html"

    def get(self, request, orderno):
        context = {
            "order": DispatchOrder.objects.get(orderno=orderno),
            "items": DispatchItem.objects.filter(orderno=orderno),
            "orderdetails": DispatchOrderDetails.objects.get(orderno=orderno),
            "order_base": self.order_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, orderno):
        form = DispatchDetailsForm(request.POST)
        if form.is_valid():
            orderdetailsobj = DispatchOrderDetails.objects.get(orderno=orderno)

            orderdetailsobj.eway = request.POST.get("eway")
            orderdetailsobj.veh = request.POST.get("veh")
            orderdetailsobj.destination = request.POST.get("destination")
            orderdetailsobj.po = request.POST.get("po")
            orderdetailsobj.cgst = request.POST.get("cgst")
            orderdetailsobj.sgst = request.POST.get("sgst")
            orderdetailsobj.igst = request.POST.get("igst")
            orderdetailsobj.cess = request.POST.get("cess")
            orderdetailsobj.tcs = request.POST.get("tcs")
            orderdetailsobj.total = request.POST.get("total")
            orderdetailsobj.save()
            messages.success(
                request, "Los detalles de despacho hans sido modificados correctamente"
            )
        context = {
            "order": DispatchOrder.objects.get(orderno=orderno),
            "items": DispatchItem.objects.filter(orderno=orderno),
            "orderdetails": DispatchOrderDetails.objects.get(orderno=orderno),
            "order_base": self.order_base,
        }
        return render(request, self.template_name, context)
