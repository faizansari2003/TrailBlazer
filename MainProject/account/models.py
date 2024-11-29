from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=10,default=9999999999)
    dob = models.DateField(default=None)

    def __str__(self):
        return f'{self.user.username} | Customer User Id - {self.user.id}'

STATE_CHOICES = [
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CT', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
    ('AN', 'Andaman and Nicobar Islands'),
    ('CH', 'Chandigarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DL', 'Delhi'),
    ('JK', 'Jammu and Kashmir'),
    ('LA', 'Ladakh'),
    ('LD', 'Lakshadweep'),
    ('PY', 'Puducherry'),
]

class Address(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=100,default="unknown")
    address_line_2 = models.CharField(max_length=100,default="unknown")
    city = models.CharField(max_length=100,default="unknown")
    pincode = models.PositiveIntegerField(default=666666,blank=True)
    state = models.CharField(max_length=2,choices=STATE_CHOICES)
    is_selected = models.BooleanField(default=False) 

    def __str__(self):
        return f'{self.user} | {self.title} '