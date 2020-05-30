from accounts.forms import (
        AdminCreationForm ,
        AccountUpdateForm,
        AccountAutheticationForm
)
from blog.models import BlogPost
from blog.views import search
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate ,logout , login 
from operator import attrgetter


# Create your views here.


def account_view(request):
    context = {}
    # to enable search bar in account view
    if request.GET:
        return search(request)

    # code for update acount
    if not request.user.is_authenticated:
        return redirect("Accounts:login")

    if request.POST:
        form = AccountUpdateForm(request.POST,instance= request.user)
        if form.is_valid():
            form.initial = {
                "email"     : request.POST['email'],
                "name"      : request.POST['name'],
                "contact"   : request.POST['contact']
            }
            form.save()
            context['message'] = "Your Account is Updated"
    else:
        form = AccountUpdateForm(
            initial = {
                "email" : request.user.email,
                "name" : request.user.name,
                "contact" : request.user.contact,
            }
        )
    context['update_form'] = form 
    blog_posts = BlogPost.objects.filter(author = request.user)
    context['blog_post'] = blog_posts

    return render(request , 'accounts/acount.html' , context)

def logout_view(request):
    logout(request)
    return redirect('home:home')

def login_view(request):
    context = {}

    user = request.user
    
    if request.GET:
        return search(request)

    if user.is_authenticated:
        return redirect("home:home")
    
    if request.POST:
        form = AccountAutheticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            pasword = request.POST['password']
            user = authenticate(email = email , password = pasword)
            if user:
                login(request , user)
                return redirect("home:home")
    
    else:
        form = AccountAutheticationForm()
    
    context['login_form'] =form
    return render(request , 'accounts/login.html' ,context)

def RegisterView(request):
    context = {}
    
    if request.GET:
        return search(request)
    
    if request.POST:
        form = AdminCreationForm(request.POST or None)
        if form.is_valid():
          
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email= email , password = raw_password)
            login(request, account)
            return redirect('home:home')
        else:
            form.initial = {
                "email"     : request.POST['email'],
                "name"      : request.POST['name'],
                "contact"   : request.POST['contact']
            }
            context['form'] = form
    else:
        context['form'] = AdminCreationForm()
        
    return render(request , 'accounts/register.html',context )

def user_account_info(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("Accounts:login")

    blog = sorted(BlogPost.objects.filter(author = request.user), key=attrgetter('date_updated'), reverse=True)
    context["blogs"] = blog
    return render(request,"accounts/snippets/blog_user_view.html",context)