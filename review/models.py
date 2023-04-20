from django.db import models
from authentication.models import User
from food_app.views import food_box_func,soup_box_func

# Create your models here.


class ReviewModel(models.Model):
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    food_type = models.CharField(max_length=100, choices=[("food", "Food"),("soup", "Soup")])
    
    
    def get_food(self):
        food_box = []
        soup_box = []
        try:
            if self.food_type == "food":
                food = food_box_func()
                for item in food:
                    food_box.append(item[1])
                food_box = food_box
                #food_model = models.CharField(max_length=100, choices=[food_box])
                return food_box
        except:
            pass
        else:
            try:
                soup = soup_box_func()
                for item in soup:
                    soup_box.append(item[1])
                soup_box = soup_box
                #soup_model = models.CharField(max_length=100, choices=[soup_box])
                return soup_box
            except:
                pass

    food = models.CharField(max_length=100, choices=get_food(food_type))