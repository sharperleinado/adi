from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import User 


class EmailorUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username, password=None, **kwargs):
        
        user_model = User

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        
        users = user_model._default_manager.filter(Q(**{user_model.USERNAME_FIELD: username}) | Q(email__iexact=username))


        for user in users:
            if user.check_password(password):
                return user 


        #if not users:
         #   user_model().set_password(password)


        



        