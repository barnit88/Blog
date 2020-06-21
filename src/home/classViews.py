from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from operator import attrgetter
from django.core.paginator import EmptyPage ,PageNotAnInteger , Paginator
from blog.views import get_blog_queryset

from blog.models import BlogPost

#simple as function based view
class HomeListView(ListView):
    model = BlogPost
    #yo queryset ra get_queryste leh autai kaam garxa
    # queryset = sorted(BlogPost.objects.all(), key=attrgetter('date_updated'), reverse=True)
    # queryset= BlogPost.objects.all()
    paginate_by = 3
    template_name = "home/home.html"

    def get_queryset(self):
        return BlogPost.objects.all()

    #malai extra context haru pathauna manlagyo bhaney esare pathauna milxa
    #below method contains pagination
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        queryblog=""
        if self.request.GET:
        	queryblog = self.request.GET.get('q',"")
        context['query'] = str(queryblog)
        
        blog_posts = sorted(get_blog_queryset(queryblog), key=attrgetter('date_updated'), reverse=True)
        #pagination starts from here
        blog_post_paginator = Paginator(blog_posts, self.paginate_by)
        page = self.request.GET.get('page' , 1)
        try:
            blogs = blog_post_paginator.page(page)
        except PageNotAnInteger:
            blogs = blog_post_paginator.page(page)
        except EmptyPage:
            blogs = blog_post_paginator.page(Paginator.num_pages)

        context['blogs'] = blogs
        context['name'] ="Checking"
        context['publisher'] = "Hello My name is Barnit Basnet"
        return context

