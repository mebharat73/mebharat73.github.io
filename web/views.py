from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm 
#from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile, Post
from .forms import CreateBlogForm, CategoryForm


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home_page")
        else:
            return render(request, "main/add_category.html", {'form':form})
        
    else:
        form = CategoryForm()
        return render(request, "main/add_category.html", {'form':form})


def create_post(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST)
        if form.is_valid():
            
            form.save(author = request.user)
    
            return redirect("home_page")
        
        else:
            return render(request, "main/create_blog.html", {'form':form})
        
    else:
        form = CreateBlogForm()
        return render(request, "main/create_blog.html", {'form':form})



def home(request):
    latest_blogs = Post.objects.all().order_by('-created_at')

    context={
        'blogs':latest_blogs
    }
    return render(request,'main/home.html', context)

def post_view(request):
    return render(request, 'main/post.html')


#............................................................................................................................

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:
            user = authenticate(request, username=username, password=password)
        except User.DoesNotExist:
            return render(request, 'main/login.html', {'error':'Invalid credential'})
        else:
            if user is None:
                return render(request, 'main/login.html', {'error':'Invalid parameter'})
            else:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(7*24*60*60)
                return redirect("home_page")
    else:
        return render(request, 'main/login.html')




#*********************************************************************************

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        try:
            user=User.objects.get(username=username)
            return render (request, 'main/signup.html', {'error':"username must be unique"})
        except User.DoesNotExist:
            if len(username) <6 and '@' not in username:
                return render(request, 'main/signup.html', {'error':"username mst be atleast 6 character and contain @"})
            elif password != password_confirm:
                return render(request, 'main/signup.html', {'error':"Password and Confirm password must be same"})
            elif len(password)<6 and len(password_confirm)<6:
                return render(request, 'main/signup.html', {'error':"password must be 6 character long"})
            else:
                first_name = request.POST.get('first_name', 'default_name')
                last_name = request.POST.get('last_name', 'default_name')
                profile_pic = request.FILES.get('profile_picture')
                user = User.objects.create_user(username, password=password, first_name=first_name, last_name=last_name)

                if profile_pic:
                    Profile.objects.create(profile_pic=profile_pic, user=user)
                return redirect('login_page')
    else:
        return render(request, 'main/signup.html')



#...................................................................................................................................


def contact_view(request):
    return render (request, 'main/contact.html')

#...................................................................................................................................


def logout_view(request):
    logout(request)
    return redirect("home_page")

#....................................................................
