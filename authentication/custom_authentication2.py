from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import User 


class EmailorUsernameModelBackend(ModelBackend):

    def authenticate(self, request, username, password, **kwargs):

        if '@' in username:
            kwargs = {'email':username}
        else:
            kwargs = {'username':username}
        
        user = User.objects.get(**kwargs)
        try:
            if user.check_password(password):
                return user 

        except user.DoesNotExist:
            return None 

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)

        except:
            return None


    
