from django.urls import path 
from blog.classViews import(
   BlogDetailView,
   BlogCreateView,
   BlogUpdateView,
   BlogDeleteView
)
from blog.views import(
    must_authenticate_view,
    
    delete_blog_view
)

app_name= "blog"

urlpatterns = [
    path('create/',BlogCreateView.as_view() , name = 'create' ),
    path('must_authenticate/',must_authenticate_view , name = 'must_authenticate' ),
    path('<slug>/',BlogDetailView.as_view() , name = 'detail' ),
    path('<slug>/delete',BlogDeleteView.as_view() , name = 'delete' ),
    path('<slug>/edit/',BlogUpdateView.as_view(), name = 'edit' ),
]