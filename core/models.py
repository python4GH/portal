from django.db import models
from django.urls import reverse
import secrets
from django.contrib.auth.models import User
from .paystack import PayStack
from trisolace.models import Product, Customer


# Create your models here.

class Payment(models.Model):
    

    name = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    duration = models.CharField(max_length=200, null=True)
    amount = models.PositiveIntegerField(default='0')
    email = models.EmailField(default=" ")
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"{self.name} -{self.product} - GH₵ {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref).first()
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            self.paystack_response = result
            if result["amount"] / 100 == self.amount:
                self.completed = True
            self.save()
            return True
        return False

# Create your models here.
