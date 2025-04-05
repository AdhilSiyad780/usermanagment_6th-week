from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
import re

# Create your views here.
@never_cache
def Login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,'myadmin.html')
        else:
            return redirect('home')
    error=''                    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('myadmin')
            else:
                return redirect('home')
        else:
            error = "username or password is incorrect"
    return render(request,"login.html",{"message": error})
#--------------------------------------------------------------------------------------------
@never_cache
def signup(request):
    error =''
    
    if request.user.is_authenticated:
        return render(request,'home.html')
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
 #----------------------------password---------------------------------------------------------------   
        if len(password1) < 8:
            error = 'Password must be at least 8 characters long.'
            return render(request,'signup.html',{ 'passerror':error})
        elif not any(char.isupper() for char in password1):
            error = 'Password must contain at least one uppercase letter.'
            return render(request,'signup.html',{ 'passerror':error})
        elif not any(char.islower() for char in password1):
            error = 'Password must contain at least one lowercase letter.'
            return render(request,'signup.html',{ 'passerror':error})
        elif not any(char.isdigit() for char in password1):
            error = 'Password must contain at least one digit.'
            return render(request,'signup.html',{ 'passerror':error})
        elif not any(char in "!@#$%^&*()_" for char in password1):
            error = 'Password must contain at least one special character.'
            return render(request,'signup.html',{ 'passerror':error})
        elif password1!=password2:
            error = 'your passwords does not match'
            return render(request,'signup.html',{ 'passerror':error})
        
#-----------------------------username---------------------------------------------------------------
        if User.objects.filter(username=username).exists():
            error = 'This username already already exists'
            return render(request,'signup.html', { 'usererror':error})
#--------------------email----------------------------------------------------------------------------
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            error = 'Enter a valid email address.'
            return render(request,'signup.html',{'emailerror:error'})
        if User.objects.filter(email=email).exists():
            error = 'This email already already exists'
            return render(request,'signup.html', { 'emailerror':error})
        
        user = User.objects.create_user(username,email,password1)
        user = user.save()
        messages.success(request, 'User has been created successfully')

        return redirect('Login')
    return render(request,'signup.html')



#------------------------------------------------------------------
@never_cache
def home(request):
    if request.user.is_superuser:
        return render(request,'myadmin.html')
    if request.user.is_authenticated:
        return render(request,'home.html')
    return render(request,"login.html")
#-----------------------------------------------------------------------------
def Logout(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            logout(request)
            return redirect('Login')
        return redirect('home')
    return render(request,'login.html')   
#====================================admin=================================admin======================
@never_cache
def my_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        search = request.GET.get('search','')
        print(search)
        if search:
            users = User.objects.filter(
                Q(username__icontains = search) | Q(email__icontains = search))
        else:
            users = User.objects.all()
        return render(request,'myadmin.html',{'users':users})
    return redirect('Login')
#----------------------------------------------------------------------------------------
@never_cache
def edit_user(request,user_id):
    if request.user.is_authenticated and request.user.is_superuser:
        user =get_object_or_404(User,id=user_id)
        if request.method == 'POST':
            error = ''
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exclude(id=user_id).exists():
                error = ' username already  exists'
                return render(request,'edituser.html',{'usererror':error})
            elif User.objects.filter(email=email).exclude(id=user_id).exists():
                error = 'Email already exists'
                return render(request,'edituser.html',{'mailerror':error})
            if not error:
                user.username=username
                user.email=email
                if password:
                    user.set_password=password
                user.save()
            return redirect('myadmin')
            

    return render(request,'edituser.html',{'user':user })
#-----------------------------------------------------------------------------------------
@never_cache
def add_user(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(username,email,password)
#---------------------------email--------------------------------------------------
            if User.objects.filter(email=email).exists():
                error = 'This email already already exists'
                return render(request,'adduser.html', { 'emailerror':error}) 
            if not password:
                error = 'your passwords is mantatory'
                return render(request,'adduser.html',{ 'passerror':error})
            if len(password) < 8:
                error = 'Password must be at least 8 characters long.'
                return render(request,'adduser.html',{ 'passerror':error})
            elif not any(char.isupper() for char in password):
                error = 'Password must contain at least one uppercase letter.'
                return render(request,'adduser.html',{ 'passerror':error})
            elif not any(char.islower() for char in password):
                error = 'Password must contain at least one lowercase letter.'
                return render(request,'adduser.html',{ 'passerror':error})
            elif not any(char.isdigit() for char in password):
                error = 'Password must contain at least one digit.'
                return render(request,'adduser.html',{ 'passerror':error})
            elif not any(char in "!@#$%^&*()_" for char in password):
                error = 'Password must contain at least one special character.'
                return render(request,'adduser.html',{ 'passerror':error})
#--------------------------pasword------------------------------------
            if User.objects.filter(username=username).exists():
                error = 'This username already already exists'
                return render(request,'adduser.html', { 'usererror':error})
            
#-------------------------username--------------------------------------------
            else:
                User.objects.create_user(username=username,email=email,password=password)
            return redirect('myadmin')

        return render(request,'adduser.html')
#-----------------------------------------------------------------------------------------------
@never_cache
def delete_user(request,user_id):
    if request.user.is_superuser and request.user.is_authenticated:
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, 'User has been deleted successfully')
        return redirect('myadmin')
      
    return render(request,'myadmin.html')

 
   
   
       
