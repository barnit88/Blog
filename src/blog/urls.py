from django.urls import path 
from blog.views import(
    create_blog_view,
    must_authenticate_view,
    detail_blog_view,
    edit_blog_view,
    delete_blog_view
)

app_name= "blog"

urlpatterns = [
    path('create/',create_blog_view , name = 'create' ),
    path('must_authenticate/',must_authenticate_view , name = 'must_authenticate' ),
    path('<slug>/',detail_blog_view , name = 'detail' ),
    path('<slug>/delete',delete_blog_view , name = 'delete' ),
    path('<slug>/edit/',edit_blog_view, name = 'edit' ),
]