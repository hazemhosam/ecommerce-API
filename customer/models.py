from django.db import models
from django.conf import settings
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    birthdate = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}' 
    
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 related_name='addresses')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.address}, {self.city}, {self.state}'    
