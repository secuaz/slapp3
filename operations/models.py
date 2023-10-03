from django.db import models
from inventory.models import Stock


class ProductionMachine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductionOrder(models.Model):
    orderno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    machine = models.ForeignKey(
        ProductionMachine, on_delete=models.CASCADE, related_name="productionmachine"
    )

    def __str__(self):
        return "Orden nro: " + str(self.orderno)

    def get_items_list(self):
        return ProductionItem.objects.filter(orderno=self)


class ProductionItem(models.Model):
    orderno = models.ForeignKey(
        ProductionOrder, on_delete=models.CASCADE, related_name="productionorderno"
    )
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="productionitem"
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "Orden nro: " + str(self.orderno.orderno) + ", Item = " + self.stock.name


class ProductionOrderDetails(models.Model):
    orderno = models.ForeignKey(
        ProductionOrder, on_delete=models.CASCADE, related_name="productiondetailsorderno"
    )

    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)

    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return "Orden nro: " + str(self.orderno.orderno)


class DispatchOrder(models.Model):
    orderno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return "Orden nro: " + str(self.orderno)

    def get_items_list(self):
        return DispatchItem.objects.filter(orderno=self)


class DispatchItem(models.Model):
    orderno = models.ForeignKey(
        DispatchOrder, on_delete=models.CASCADE, related_name="dispatchorderno"
    )
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="dispatchitem")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "Orden nro: " + str(self.orderno.orderno) + ", Item = " + self.stock.name


class DispatchOrderDetails(models.Model):
    orderno = models.ForeignKey(
        DispatchOrder, on_delete=models.CASCADE, related_name="dispatchdetailsorderno"
    )

    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)

    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return "Orden nro: " + str(self.orderno.orderno)
