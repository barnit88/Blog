#shortcuts
from django.shortcuts import render ,get_object_or_404 ,redirect
#Generic Views
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
#forms
from blog.forms import CreateBlogPostForm ,UpdateBlogPostForm 
#neccessary impoort
from operator import attrgetter
from django.core.paginator import EmptyPage ,PageNotAnInteger , Paginator
from django.db.models import Q
#models
from .models import BlogPost
from accounts.models import Account


def searchbar(request):
    print("Hello")
    context = {}    
    
    query = ""  
    BLOG_POSTS_PER_PAGE = 2
    if request.GET:
    	query = request.GET['q']
    	context['query'] = str(query)
    
    blog_posts = sorted(get_blog_queryset_class_view(query), key=attrgetter('date_updated'), reverse=True)
    context['blogs'] = blog_posts   
    
    # With Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
    try:
    	blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
    	blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
    	blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)  
    context['blogs'] = blog_posts  

    return render(request, "home/home.html", context)

def get_blog_queryset_class_view(query=None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		posts = BlogPost.objects.filter(
			Q(title__icontains=q) |
			Q(body__icontains=q)
			).distinct()
		for post in posts:
			queryset.append(post)

	# create unique set and then convert to list
	return list(set(queryset))   



#Custom MIxins Provide search
class Mixin(object):
    
    def get_search_query(self):
        if self.request.GET.get('q'):
            return searchbar(self.request)

    #THis context is only for Detail
    def get_context_data(self):
        context = {} 
        slug = self.kwargs.get('slug')
        print(slug)
        blog_post = get_object_or_404(BlogPost , slug=slug )
        context['blog_post'] = blog_post
        context["check"] = "Checking"
        return render(self.request,'blog/detail_blog.html' ,context)  
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(BlogPost ,slug=slug)
        return obj

    def author_object(self):
        user = self.request.user
        obj = get_object_or_404(Account , pk = user.id)
        return obj



class BlogDetailView(Mixin ,DetailView):
    model = BlogPost
    template_name = 'blog/detail_blog.html'

    def get(self, request , **kwargs):
       #search bar
        if self.request.GET.get('q'):
            search_query = self.get_search_query()
            return search_query
        detail_query = self.get_context_data()
        return detail_query


class BlogCreateView(LoginRequiredMixin,Mixin ,CreateView):
    login_url = '/register/login/'
    model = BlogPost
    # form_class = CreateBlogPostForm
    template_name = 'blog/create_blog.html'
    
    # Create your views here.
    def get(self , request , **kwargs):
        context= {}
        if self.request.GET.get('q'):
            search_query = self.get_search_query()
            return search_query
        user = request.user
        print(user ,"checking user")
        if not user.is_authenticated:
            return redirect('blog:must_authenticate')
        form = CreateBlogPostForm() 
        context['form'] = form
        return render(request,"blog/create_blog.html" , context)

    def post(self, request ,*args , **kwargs):       
        context= {}
        form = CreateBlogPostForm(request.POST or None , request.FILES or None)
        user = self.author_object()
        if not user.is_authenticated:
            return redirect('blog:must_authenticate')    
        if form.is_valid():
            obj = form.save(commit=False)
            # author = Account.objects.filter(email = user.email).first()
            # author = get_object_or_404(Account , pk = user.id)
            author = self.author_object()   #three diffrent way 
            print(author ,"Authro prngasda")
            obj.author = author
            obj.save()
            context['message']  = "Blog Upload .Successful!!" 
            form = CreateBlogPostForm()
        context['form'] = form
        return render(request,"blog/create_blog.html" , context)


class BlogUpdateView(LoginRequiredMixin,Mixin ,UpdateView):
    login_url = '/register/login/'
    model = BlogPost
    # form_class = CreateBlogPostForm
    template_name = 'blog/create_blog.html'
    
    # Create your views here.
    def get(self , request , **kwargs):
        context= {}
        if self.request.GET.get('q'):
            search_query = self.get_search_query()
            return search_query
        blog_post = self.get_object()
        user = self.author_object()
        if not user.is_authenticated:
            return redirect('blog:must_authenticate')
        form =UpdateBlogPostForm(
            initial={
                "title": blog_post.title,
                "body": blog_post.body,
                "image": blog_post.image,
            }
        )
        context['form'] = form
        context['blog']= blog_post
        return render(request,"blog/edit_blog.html" , context)

    def post(self, request ,*args , **kwargs):       
        context= {}
        user = self.author_object()
        if not user.is_authenticated:
            return redirect('blog:must_authenticate')    
        
        blog_post = self.get_object()
        form = CreateBlogPostForm(request.POST or None , request.FILES or None , instance = blog_post)
        
        if user.email == blog_post.author.email:
            if form.is_valid():
                obj = form.save(commit=False)
                # author = Account.objects.filter(email = user.email).first()
                # author = get_object_or_404(Account , pk = user.id)
                author = self.author_object()   #three diffrent way 
                obj.author = author
                obj.save()
                context['message']  = "Blog Upload .Successful!!" 
                form = CreateBlogPostForm()
            context['form'] = form
            return render(request,"blog/create_blog.html" , context)
        

class BlogDeleteView(LoginRequiredMixin,Mixin ,DeleteView):
    login_url = '/register/login/'
    # form_class = CreateBlogPostForm
    template_name = 'blog/delete_content.html'
    
    def get(self, request,**kwargs):
        context = {}
        blog_post = self.get_object()
        context["blog_post"] = blog_post
        return render(request,"blog/delete_content.html" ,context)


    # Create your views here.
    def post(self, request ,*args , **kwargs):   
        user = request.user
        blog_post = self.get_object()
        if not user.is_authenticated:
            return redirect('blog:must_authenticate')
        if user.email == blog_post.author.email:
            if self.request.POST :
                blog_post = self.get_object()
                blog_post.delete()
                return redirect('home:home')
       

