from django.urls import path
from home.classViews import HomeListView

app_name= "home"

urlpatterns = [
    path('', HomeListView.as_view(),name = "home")
]
