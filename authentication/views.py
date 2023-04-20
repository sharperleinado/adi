from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from my_site.settings import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string,get_template
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token
from .models import User 
from django.contrib.auth.password_validation import password_changed,validate_password,UserAttributeSimilarityValidator,CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator
from .custom_authentication import EmailorUsernameModelBackend
from .forms import MobileForm,EmailReset
from .models import Mobile
from django.urls import reverse 
from .forms import UpdateMobileForm
from django.db.models import Q

#from .custom_authentication2 import EmailorUsernameModelBackend


# Create your views here.

def email_reset_password(request):
    form = EmailReset()
    if request.method == "POST":
        form = EmailReset(request.POST)
        if form.is_valid():
            username_or_mail = form.cleaned_data["email"].strip()
            try:
                model = User.objects.get(Q(username=username_or_mail) | Q(email=username_or_mail))

                #Email Password reset
                try: 
                    current_site = get_current_site(request) 
                    email_subject = 'Password reset @ADimealsmobile!'
                    message2 = render_to_string('email_password_reset.html',{
                        'name':model.first_name,
                        'domain':current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(model.pk)),
                        'token': generate_token.make_token(model)
                    }) 
                    from_email2 = EMAIL_HOST_USER
                    to_list2 = [model.email]
                    email2 = EmailMessage(
                        email_subject,
                        message2,
                        from_email2,
                        to_list2,
                    )
                    email2.content_subtype = "html"
                    fail_silently = False
                    email2.send()
                    messages.success(request, "We have sent RESET PASSWORD link to your registered email address to rest your password!")
                    return redirect('authentication:email_reset_password')
                except:
                    return render(request, 'authentication/connection_error.html',{'fname':model.first_name})
                    #messages.error(request, "There was an error in connection. Please try again!")
                    #return redirect('authentication:email_reset_password')
                    #messages.success(request, "We have sent RESET PASSWORD link to your registered email address to rest your password!")
                    #return redirect('authentication:email_reset_password')
            except:
                messages.error(request, "User details does not exist in our database! Be sure to input a correct email or username.")
                return redirect('authentication:email_reset_password')

    return render(request,'authentication/email_reset.html',{'form':form})



def mobile(request):
    #I first created a form to get phone number input from user, then render the number as per the currrent user request in the account info template.
    instance = ""
    form = ""
    try:
        form = MobileForm()
        if request.method == "POST":
            form = MobileForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request, "You have successfully uploaded a phone number!")
                return redirect('address:billing_address')
    except:
        pass

    return render(request,'authentication/mobile.html',{'form':form})


def main(request):
    fname = ""
    try:
        fname = request.user.first_name
    except AttributeError:
        return redirect('authentication:signin')
    
    return render(request,'authentication/landing_page.html',{'fname':fname})


def all(request):

    return render(request,'authentication/all_signups.html')


def signup(request):

    if request.method == "POST":
        username = request.POST.get("username").strip()
        fname = request.POST.get("fname").strip()
        lname = request.POST.get("lname").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        password2 = request.POST.get("password2").strip()


        if User.objects.filter(username=username):
            messages.error(request, "Username already exist!")
            return redirect('authentication:signup')
        
        elif User.objects.filter(email=email):
            messages.error(request, "E-mail already exist!")
            return redirect('authentication:signup')
            
        elif len(username) > 15:
            messages.error(request, "Length of username too long!")
            return redirect('authentication:signup')

        elif password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('authentication:signup')


        elif password:
            try:
                UserAttributeSimilarityValidator().validate(password)
            except:
                messages.error(request,"Password too similar to user attribute provided.\nPlease, try another password!")
                return redirect('authentication:signup')
            try:
                CommonPasswordValidator().validate(password)
            except:     
                messages.error(request,"Password too common and easy.\nPlease, try another password!")
                return redirect('authentication:signup')
            try:
                MinimumLengthValidator().validate(password)
            except:
                messages.error(request,"Only a minimum characters of 8 is allowed.\nPlease, try another password!")
                return redirect('authentication:signup')
            try:
                NumericPasswordValidator().validate(password)
            except:
                messages.error(request,"Numeric only password is not allowed.\nPlease, try another password!")
                return redirect('authentication:signup')

        
            user = User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password)
            user2 = User.objects.get(username=username)
            #Daniel, do not forget to set user.is_active = False during deployment.
            user.is_active = True
        
            #Welcome mail
            try:
                email_subject = 'Welcome mail @ADimealsmobile!'
                message = render_to_string('welcome_mail.html',{
                    'name':fname
                }) 
                from_email = EMAIL_HOST_USER
                to_list = [user2.email]
                email = EmailMultiAlternatives(
                    email_subject,
                    message,
                    from_email,
                    to_list,
                )
                email.content_subtype = "html"
                fail_silently = True
                email.send()
            except:
                return render(request, 'authentication/connection_error.html',{'fname':fname})
                #messages.error(request, "There was an error in connection. Please try again!")
                #return redirect('authentication:signup')

            # Welcome E-mail
            #try:
            #    subject = 'Welcome to ADi meals mobile!'
            #    message = f'Hello {fname.capitalize()}, welcome to ADi meals mobile!\n\nThank you for visiting our website.\n\nWe have also sent you a confirmation email, please confirm your email address to login into your account.\n\n\n\nThanking you.\n\n\nVictoria Oluwaseyi\nC.E.O'
            #    from_email = EMAIL_HOST_USER
            #    to_list = [user2.email]
            #    send_mail(subject,message,from_email,to_list,fail_silently=False)
            #except:
            #    return render(request, 'authentication/connection_error.html',{'fname':fname})
                

            #Email Confirmation
            try: 
                current_site = get_current_site(request) 
                email_subject = 'Email confirmation @ADimealsmobile!'
                message2 = render_to_string('email_confirmation.html',{
                    'name':fname,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user2.pk)),
                    'token': generate_token.make_token(user2)
                }) 
                from_email2 = EMAIL_HOST_USER
                to_list2 = [user2.email]
                email2 = EmailMultiAlternatives(
                    email_subject,
                    message2,
                    from_email2,
                    to_list2,
                )
                email2.content_subtype = "html"
                fail_silently = True
                email2.send()

                messages.success(request,"Your account has been successfully created!\nWe have also sent you a confirmation email, please confirm your email address to login into your account.")
                return redirect('authentication:signin')
        
            except:
                return render(request, 'authentication/connection_error.html',{'fname':fname})
                #messages.error(request, "There was an error in connection. Please try again!")
                #return redirect('authentication:signup')
                #messages.success(request,"Your account has been successfully created!\nWe have also sent you a confirmation email, please confirm your email address to login into your account.")
                #return redirect('authentication:signin')

    return render(request,'authentication/signup.html')


def signin(request):
    
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        remember_me = request.POST.get("checkbox")

        user = EmailorUsernameModelBackend.authenticate(EmailorUsernameModelBackend,request,username,password)
        #Daniel, do not forget to add "and user.is_active == False during deployment"
        if user is not None: #and user.is_active == False:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(None)
                
            messages.success(request, "You have successfully logged in")
            return redirect('authentication:account_info')

        else:
            messages.error(request, "Bad credentials! or Check your mail to verify account if you have not!")
            return redirect('authentication:signin')


    return render(request,'authentication/signin.html')


def signout(request):

    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,user.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True 
        fname = user.fname 
        user.save()
        login(request, user)
        messages.success(request, "Email has been verified successfully!")
        return render(request,'home.html',{'fname':fname})
    else:
        return render(request, 'activation_failed.html')
    

def activate2(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,user.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        return redirect(reverse('authentication:reset',args=[uid,token]))

    else:
        return render(request, 'activation_failed.html')

        

def account_info(request):
    #This is a view that displays the current information of the user!
    #It displays the username, first name, last name and email. it also gives the user access to edit the account information.
    try:
        uname = ""
        fname = ""
        lname = ""
        email = ""
    
        uname = request.user.username
        fname = request.user.first_name
        lname = request.user.last_name
        email = request.user.email
    except AttributeError:
        return redirect('authentication:signin')
    
    try:
        phone = Mobile.objects.get(user=request.user)
    except AttributeError:
        messages.error(request, "Please, kindly input your ACTIVE PHONE NUMBER to better help our delivery man reach you.")
        return redirect(reverse('authentication:mobile'))
    except:
        messages.error(request, "Please, kindly input your ACTIVE PHONE NUMBER to better help our delivery man reach you.")
        return redirect(reverse('authentication:mobile'))

    return render(request,'authentication/account_info.html',{'names':[uname,fname,lname,email,phone]})


def edit_account(request):
    #This is a view to edit a user's account information

    #What I did here is, I first of all listed out all the details of the user currently logged in 
    #Then I got all the user inputs from the "Edit info template"
    #After which I got the User object, then inserted each new input from edit info template.

    #Here I added a Phone number form to this view to update phone number    
    try:
        form = UpdateMobileForm()
        if request.method == "POST":
            form = UpdateMobileForm(request.POST)
            if form.is_valid():
                model = Mobile.objects.get(user=request.user)
                model.user = request.user 
                model.phone_no = form.cleaned_data["phone_no"]
                model.save()
                messages.success(request, "You have successfully updated your PHONE NUMBER!")
                return redirect('authentication:account_info')
    except AttributeError:
        #pass
        return redirect('authentication:signin')

    try:
        user_uname = request.user.username
        user_fname = request.user.first_name
        user_lname = request.user.last_name
        user_email = request.user.email
    
        user = User.objects.get(username=user_uname)
    
        if request.method == "POST":
            uname = request.POST.get("username").strip()       
            fname = request.POST.get("fname").strip()
            lname = request.POST.get("lname").strip()
            email = request.POST.get("email").strip()

            if User.objects.filter(username=uname):
                messages.error(request, "Username has been taken!\nPlease, try another username.")
                return redirect('authentication:edit_account')
            elif User.objects.filter(email=email):
                messages.error(request, "Email has been taken!\nPlease, try another Email.")
                return redirect('authentication:edit_account')

            if uname == "":
                uname = user_uname
            else:
                user.username = uname
                user.save()
            if fname == "":
                fname = user_fname 
            else:
                user.first_name = fname 
                user.save()
            if lname == "":
                lname = user_lname
            else:
                user.last_name = lname
                user.save()
            if email == "":
                email = user_email
            else:
                user.email = email
                user.save()
            
            messages.success(request, "You have successfully updated your account details!")
            return redirect('authentication:account_info')
    except AttributeError:
        return redirect('authentication:signin')
        
    return render(request,'authentication/edit_account.html',{'form':form})


#This is a page to reset password while user is logged in 
def setpassword(request):
    try:
        username = request.user.username
        if request.method == "POST":
            password = request.POST.get("password").strip()
            password2 = request.POST.get("password2").strip()

            user = User.objects.get(username=username)
    
            if password:
            
                if password != password2:
                    messages.error(request,"Passwords do not match!")
                    return redirect('authentication:setpassword')
                
                try:
                    UserAttributeSimilarityValidator().validate(password)
                except:
                    messages.error(request,"Password too similar to user attribute provided.\nPlease, try another password!")
                    return redirect('authentication:setpassword')
                try:
                    CommonPasswordValidator().validate(password)
                except:
                    messages.error(request,"Password too common and easy.\nPlease, try another password!")
                    return redirect('authentication:setpassword')
                try:
                    MinimumLengthValidator().validate(password)
                except:
                    messages.error(request,"Only a minimum characters of 8 is allowed.\nPlease, try another password!")
                    return redirect('authentication:setpassword')
                try:
                    NumericPasswordValidator().validate(password)
                except:
                    messages.error(request,"Numeric only password is not allowed.\nPlease, try another password!")
                    return redirect('authentication:setpassword')
                try:
                    password_changed(password,user=User,password_validators=NumericPasswordValidator)
                except:
                    messages.error(request, "Old password cannot be used!\nPlease, try a new password.")
                    return redirect('authentication:setpassword')


                user.set_password(password)
                user.save()
                messages.success(request, "You have successfully changed your password!")
                return redirect('authentication:signin')
    except AttributeError:
        return redirect('authentication:signin')
        
    return render(request,'authentication/setpassword.html')


#This is a view to reset password by e-mail or username when user forgo password 
def password_reset_by_mail(request, uid, token):
    try:
        user = User.objects.get(username=uid)
        if request.method == "POST":
            password = request.POST.get("password").strip()
            password2 = request.POST.get("password2").strip()
    
            if password:
            
                if password != password2:
                    messages.error(request,"Passwords do not match!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                
                try:
                    UserAttributeSimilarityValidator().validate(password)
                except:
                    messages.error(request,"Password too similar to user attribute provided.\nPlease, try another password!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                try:
                    CommonPasswordValidator().validate(password)
                except:
                    messages.error(request,"Password too common and easy.\nPlease, try another password!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                try:
                    MinimumLengthValidator().validate(password)
                except:
                    messages.error(request,"Only a minimum characters of 8 is allowed.\nPlease, try another password!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                try:
                    NumericPasswordValidator().validate(password)
                except:
                    messages.error(request,"Numeric only password is not allowed.\nPlease, try another password!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                try:
                   password_changed(password,user=User,password_validators=NumericPasswordValidator)
                except:
                    messages.error(request, "Old password cannot be used!\nPlease, try a new password.")
                    return redirect(reverse('authentication:reset',args=[uid,token]))


                user.set_password(password)
                user.save()
                messages.success(request, "You have successfully changed your password!")
                return redirect(reverse('authentication:reset',args=[uid,token]))
    except AttributeError:
        return redirect('authentication/connection_error.html')
        
    return render(request,'authentication/reset.html')

