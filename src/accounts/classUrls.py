from django.urls import path , include
from django.contrib.auth import views as auth_views
from .views import (
    account_view,
    RegisterView,
    logout_view,
    login_view,
    user_account_info,
)
from .classViews import (
    AccountListView,
    AccountLoginView,
    LogoutView,
    AccountCreateView,
    AccountUpdateView
)



urlpatterns = [
    path('' ,AccountCreateView.as_view() , name ="register"),
    path('account/' ,AccountUpdateView.as_view() , name ="account"),
    path('logout/' ,LogoutView.as_view() , name ="logout"),
    path('login/' ,AccountLoginView.as_view() , name ="login"),
    path('info/', AccountListView.as_view(), name= "info"),

 
    path('password_change/done/', auth_views.PasswordChangeDoneView
        .as_view(template_name = "registration/password_change_done.html"),name='password_change_done'),
    
    path('password_change/', auth_views.PasswordChangeView
        .as_view(template_name = "registration/password_change_form.html"),name='password_change'),
   
    path('password_reset/done/', auth_views.PasswordResetDoneView
        .as_view(template_name = "registration/password_reset_done.html"),name='password_reset_done'),
   
    path('password_reset/', auth_views.PasswordResetView
        .as_view() ,name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView
        .as_view(template_name = "registration/password_reset_complete.html"),name='password_reset_complete'),
   
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView
        .as_view(),name='password_reset_confirm'),
   
   

]