from django.db import models
from django.contrib.auth.models import User
from account.models import Address,Customer
from product.models import Bike
import uuid
from datetime import time

# Create your models here.
STATUS_CHOICE = [
    ('CREATED','CREATED'),
    ('PENDING','PENDING'),
    ('DISPATCHED','DISPATCHED'),
    ('PROCESSING','PROCESSING'),
    ('OUT FOR DELIVERY','OUT FOR DELIVERY'),
    ('CANCELLED','CANCELLED')
]

DELIVERY_TYPE = [
    ('EX','Express'),
    ('STD','Standard'),
    ('NG','Night')
]

class Order(models.Model):
    order_uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICE,default='PENDING',max_length=20)
    order_on = models.DateField(auto_now_add=True)
    order_time = models.TimeField(default=time(12, 0))
    last_update = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=12,decimal_places=2)
    shipping_address = models.ForeignKey(Address,on_delete=models.CASCADE,blank=True)
    shipping_charges = models.CharField(choices=DELIVERY_TYPE,default='STD',max_length=3)
    class Meta:
        ordering = ["total"]
    def __str__(self):
        return f' {self.user} | Order UUID -  {self.order_uuid}'

class OrderDetails(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Bike,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,default=15)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=12)

    def __str__(self):
        return f'{self.order.user}'