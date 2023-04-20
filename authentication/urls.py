from django.urls import path
from . import views



app_name = 'authentication'



urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('main/',views.main,name='landing_page'),
    path('create_account/',views.all,name='all_signups'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('setpassword/',views.setpassword,name='setpassword'),
    path('account_info/',views.account_info,name='account_info'),
    path('edit_account/',views.edit_account,name='edit_account'), 
    path('mobile/',views.mobile,name='mobile'),
    path('resetpasswordbymail/',views.email_reset_password,name='email_reset_password'),
    path('activate2/<uidb64>/<token>',views.activate2,name='activate2'),
    path('reset/<uid>/<token>',views.password_reset_by_mail,name='reset'),
]



