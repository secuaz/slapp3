from django import forms
from django.forms import formset_factory
from .models import (
    ProductionMachine, 
    ProductionOrder, 
    ProductionItem,
    ProductionOrderDetails, 
    DispatchOrder, 
    DispatchItem,
    DispatchOrderDetails
)
from inventory.models import Stock


# Form para seleccionar equipo
class SelectMachineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['machine'].queryset = ProductionMachine.objects.filter(is_deleted=False)
        self.fields['machine'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = ProductionOrder
        fields = ['machine']

# Form para renderizar un solo producto en formulario de produccion
class ProductionItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control quantity', 'min': '0', 'required': 'true'})
    class Meta:
        model = ProductionItem
        fields = ['stock', 'quantity']

# FORMSET para renderizar multiples productos desde --ProductionItemForm--
ProductionItemFormset = formset_factory(ProductionItemForm, extra=1)

# Form para integrar datos a los detalles de la order de produccion
class ProductionDetailsForm(forms.ModelForm):
    class Meta:
        model = ProductionOrderDetails
        fields = ['eway','veh', 'destination', 'po', 'cgst', 'sgst', 'igst', 'cess', 'tcs', 'total']


# Form para crear equipos de produccion
class MachineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'title' : 'Nombre del Equipo'})
    class Meta:
        model = ProductionMachine
        fields = ['name']


# Form para obtener los datos de cliente de despacho
class DispatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only', 'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = DispatchOrder
        fields = ['name', 'phone', 'address', 'email']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }

# Form para renderizar un solo producto en formulario de despacho
class DispatchItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
    class Meta:
        model = DispatchItem
        fields = ['stock', 'quantity']

# FORMSET para renderizar multiples productos desde --DsipatchItemForm--
DispatchItemFormset = formset_factory(DispatchItemForm, extra=1)

# Form para obtener datos de detalle en orden de despacho
class DispatchDetailsForm(forms.ModelForm):
    class Meta:
        model = DispatchOrderDetails
        fields = ['eway','veh', 'destination', 'po', 'cgst', 'sgst', 'igst', 'cess', 'tcs', 'total']
