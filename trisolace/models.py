from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)

    # bank info
    bank_account = models.CharField(max_length=200, null=True, blank=True)
    momo_number = models.CharField(max_length=200, null=True, blank=True)
    bitcoin = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}-{self.phone}"

# Create your models here.


class Product(models.Model):
    CATEGORY = (
        ('Snail-Crowdfarmings', 'Snail-Crowdfarmings'),
        ('Vegitable Farms', 'Vegitable Farms'),
    )

    category = models.CharField(max_length=200, null=True, choices=CATEGORY)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.category


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Paidout', 'Paidout'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    price = models.FloatField(null=True)
    duration = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.category



