from django import forms
from django.contrib.auth.models import Group
from accounts.models import Account
from django.contrib.auth.forms import ReadOnlyPasswordHashField ,UserCreationForm ,UserChangeForm
from django.contrib.auth import authenticate

class AdminCreationForm(UserCreationForm):
    contact = forms.CharField(help_text="Please input Your Phone Number",
        required=True,widget=forms.TextInput(attrs={'pattern':'[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]'}))

    class Meta: 
        model = Account
        fields =  ('name'  ,'contact' ,'email' ,'password1' , 'password2' )

#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don,t match")
#         return password2

#     def save(self,commit= True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password1'])
#         if commit:
#             user.save()
#         return user


# class AdminChangeForm(UserChangeForm):
#     password = ReadOnlyPasswordHashField()

#     class Meta(UserChangeForm):
#         model = Account
#         fields = ('email', 'password', 'username','name','contact' ,'is_admin' ,'is_staff' ,'is_superuser' ,'is_active')

#     def clean_password(self):
#         return self.initial["password"]

class AccountAutheticationForm(forms.ModelForm):
    password = forms.CharField(label = 'Password ' , widget= forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email','password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email = email , password = password):
                raise forms.ValidationError("Invalid Login")
        
class AccountUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ('email','name' , 'contact')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk = self.instance.pk).get(email = email)
            except Account.DoesNotExist:
               return email
            raise forms.ValidationError('Email  "%s" is already in use .' %account.email )


    def clean_name(self):
        if self.is_valid():
            name = self.cleaned_data['name']
            return name

    def clean_cotact(self):
        if  self.is_valid():
            contact = self.cleaned_data['contact']
            return contact



