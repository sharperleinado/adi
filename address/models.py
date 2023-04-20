from django.db import models
from authentication.models import User

# Create your models here.


country_choice = [("nigeria","Nigeria")]
state = [("ondo","Ondo")]
city = [("akure","Akure")]
area = [("alagbaka","Alagbaka"),("arakale","Arakale"),("araromi","Araromi"),
    ("futa north gate","Futa North Gate"),("futa south gate","Futa South Gate"),("igoba","Igoba"),
    ("ijapo","Ijapo"),("ijoka","Ijoka"),("irese","Irese"),
    ("isolo","Isolo"),("oba-ile","Oba-ile"),("oda","Oda"),
    ("oda road","Oda road"),("oke-aro","Oke-aro"),("oke-ijebu","Oke-Ijebu"),
    ("oke-ogba","Oke-Ogba"),("okuta-elerin_nla","Okuta-elerin_nla"),("onyarugbulem","Onyarugbulem"),
    ("orita","Orita-obele"),("owode","Owode"),("shagari","Shagari"),("others","Others")]

class UserAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    country = models.CharField(max_length=200, choices=country_choice)
    state = models.CharField(max_length=200, choices=state)
    city = models.CharField(max_length=200, choices=city)
    area = models.CharField(max_length=200, choices=area)
    street_name = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.street_name}, {self.area}, {self.city}."
    
    
