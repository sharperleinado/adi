from django.db import models
from django.db.models.signals import pre_save
from my_site.utils import unique_slug_generator



# Create your models here.
class Soup(models.Model):
    image = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None)
    soup_item = models.CharField(max_length=30)
    mini_box = models.DecimalField(max_digits=30,decimal_places=2)
    medium_box = models.DecimalField(max_digits=30,decimal_places=2)
    mega_box = models.DecimalField(max_digits=30,decimal_places=2)
    slug = models.SlugField(max_length=250,null=True,blank=True)

    def __str__(self):
        my_soup = f"{self.soup_item}"
        return my_soup



class Food(models.Model):
    image = models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None)
    food_item = models.CharField(max_length=30)
    food_price = models.DecimalField(max_digits=30,decimal_places=2)
    slug = models.SlugField(max_length=250,null=True,blank=True)

    def __str__(self):
        my_food = f"{self.food_item}\n\n₦{self.food_price}"
        return my_food.capitalize()
    

def slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance)
        except:
            pass

pre_save.connect(slug_generator, sender=Food)
pre_save.connect(slug_generator, sender=Soup)  

