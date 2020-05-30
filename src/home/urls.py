from django.urls import path , include
from .views import home_screen_view


app_name = 'home'

urlpatterns = [
    path('' ,home_screen_view , name ="home")
]