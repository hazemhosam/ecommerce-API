from django.db import models
from category.models import Category

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2) 
    inventory = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                  null=True,related_name='products')
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images') 
    image = models.ImageField(upload_to='product/images/')
        

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    name = models.CharField(max_length=255) 
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    rating = models.FloatField(choices=[(i, i) for i in range(1, 6)],null=True,blank=True) # get rating from 1 to 5 for a product by avg the ratinfg reviws do it in serializer and anonoite wyen quiry 
    review = models.TextField()      

    
