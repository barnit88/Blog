from accounts.models import Account
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm , UpdateBlogPostForm
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from operator import attrgetter
from django.core.paginator import EmptyPage ,PageNotAnInteger , Paginator
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required()
def create_blog_view(request):
    context = {}
    
    if request.GET:
        return search(request)

    user = request.user
    if not user.is_authenticated:
        return redirect('blog:must_authenticate')

    form = CreateBlogPostForm(request.POST or None , request.FILES or None)
    print(request.POST)
    print(request.FILES)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email = user.email).first()
        obj.author = author
        obj.save()
        context['message']  = "Blog Upload .Successful!!" 
        form = CreateBlogPostForm()
    
    context['form'] = form
    return render(request,"blog/create_blog.html" , context)


def must_authenticate_view(request):
    return render(request , 'blog/must_authenticate.html' ,{})


def detail_blog_view(request , slug):
    context = {}
    
    if request.GET:
        return search(request)

    
    blog_post = get_object_or_404(BlogPost , slug= slug)
    context['blog_post'] = blog_post

    return render(request , 'blog/detail_blog.html',context)

def delete_blog_view(request, slug):
    context = {}
    blog_post = get_object_or_404(BlogPost , slug = slug)
    context["blog_post"] = blog_post
    user = request.user
    if not user.is_authenticated:
        return redirect('blog:must_authenticate')

    if request.POST :
        blog_post = get_object_or_404(BlogPost , slug = slug)
        blog_post.delete()
        return redirect('home:home')

    return render(request,"blog/delete_content.html" ,context)

def edit_blog_view(request,slug):

    context = {}
    # Search Bar ko kaam garna lai 
    if request.GET:
        return search(request)
    # Yaha bata chai edit ko kam suru 
    user = request.user
    if not user.is_authenticated:
        return redirect('blog:must_authenticate')

    blog_post = get_object_or_404(BlogPost , slug = slug)
    if request.POST :
        form = UpdateBlogPostForm(request.POST or None , request.FILES or None , instance = blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Blog Post Updated"
            blog_post = obj
    
    form =UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "body": blog_post.body,
            "image": blog_post.image,
        }
    )
    context['blog']= blog_post
    context['form'] = form
    return render(request, 'blog/edit_blog.html' ,context )
  
def get_blog_queryset(query=None):
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

def search(request):
    context = {}    
    
    query = ""  
    BLOG_POSTS_PER_PAGE = 2
    if request.GET:
    	query = request.GET['q']
    	context['query'] = str(query)
    
    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
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


