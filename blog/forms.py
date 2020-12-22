from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,\
    UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Post

class UserSignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password(again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email': 'Email','first_name':'First Name','last_name':'Last Name'}

        widgets = {'username':forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class':'form-control'}),
                   'last_name': forms.TextInput(attrs={'class':'form-control'}),
                   'email': forms.EmailInput(attrs={'class':'form-control'})}

class UserLoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':True}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AddPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','desc']
        labels = {'title': 'Title','desc': 'Descriptions'}
        widgets = {'title': forms.TextInput(attrs={'class':'form-control'}),
                   'desc':forms.Textarea(attrs={'class':'form-control'})}

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                   'first_name':forms.TextInput(attrs={'class':'form-control'}),
                   'last_name': forms.TextInput(attrs={'class':'form-control'}),
                   'email':forms.EmailInput(attrs={'class':'form-control'})}

class ChangePassForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label='New Password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))