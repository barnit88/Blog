from accounts.forms import (
        AdminCreationForm ,
        AccountUpdateForm,
        AccountAutheticationForm
)
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
    View

)
from blog.classViews import Mixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate ,logout , login 

# Create your views here.

class AccountListView(LoginRequiredMixin,ListView):
    template_name = 'accounts/snippets/blog_user_view.html'

    def get(self , request , *args ,**kwargs):
        context = {}
        if not request.user.is_authenticated:
            return redirect("Accounts:login")
        blog = sorted(BlogPost.objects.filter(author = request.user), key=attrgetter('date_updated'), reverse=True)
        context["blogs"] = blog
        return render(request,"accounts/snippets/blog_user_view.html",context)

class AccountUpdateView(LoginRequiredMixin,Mixin,UpdateView):
    login_url = '/register/login/'
    template_name = 'accounts/acount.html'

    def get(self, request,**kwargs):
        context = {}
        # to enable search bar in account view
        if self.request.GET.get('q'):
            search_query = self.get_search_query()
            return search_query
        # code for update acount
        if not request.user.is_authenticated:
            return redirect("Accounts:login")
        form = AccountUpdateForm(
            initial = {
                "email" : request.user.email,
                "name" : request.user.name,
                "contact" : request.user.contact,
            }
        )
        context['update_form'] = form 
        return render(request , 'accounts/acount.html' , context)

    def post(self, request , *args , **kwargs):
        context = {}
        # code for update acount
        if not request.user.is_authenticated:
            return redirect("Accounts:login")
        form = AccountUpdateForm(request.POST,instance= request.user)
        if form.is_valid():
            form.initial = {
                "email"     : request.POST['email'],
                "name"      : request.POST['name'],
                "contact"   : request.POST['contact']
            }
            form.save()
            context['message'] = "Your Account is Updated"
            context['update_form'] = form 
        return render(request , 'accounts/acount.html' , context)


class AccountLoginView(Mixin ,View):

    def get(self,request,**kwargs):
        context = {}    
        user = request.user
        if request.GET.get('q'):
            search_query = self.get_search_query()
            return search_query
        if user.is_authenticated:
            return redirect("home:home")
        form = AccountAutheticationForm()
        context['login_form'] =form
        return render(request , 'accounts/login.html' ,context)

        
    def post(self, request , *args , **kwargs):
        context = {}
        # code for update acount        
        form = AccountAutheticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            pasword = request.POST['password']
            user = authenticate(email = email , password = pasword)
            if user:
                login(request , user)
                if request.GET.get('next'):
                    redirect_post_url = request.GET.get('next')
                    return redirect(redirect_post_url)
                return redirect("home:home")
        context['login_form'] =form
        return render(request , 'accounts/login.html' ,context)

class AccountCreateView(Mixin ,CreateView):

    def get(self,request , **kwargs):        
        context = {}
        if request.GET.get('q'):
            search_query = self.get_search_query()
            return search_query
        
        context['form'] = AdminCreationForm()
        return render(request , 'accounts/register.html',context )

    def post(self,request,*args,**kwargs):
        context= {}
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
        return render(request , 'accounts/register.html',context )
        
                       

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:home')

