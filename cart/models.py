from django.db import models
from authentication.models import User 
from food_app.models import Food, Soup

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
    

class CartItemsFood(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="products")
    quantity = models.IntegerField(default=1)

    def total_quantity(self):
        new_quantity = self.quantity*self.product.food_price
        return new_quantity
    
    def __str__(self):
        return self.product.food_item
    

class CartItemsSoup(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Soup, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.soup_item
    
