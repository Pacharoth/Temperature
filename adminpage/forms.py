from django import forms
from adminpage.models import RoomServer,ProfileUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#login form
class loginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'style':'border: 1px solid #dddfe2;','placeholder':'Username'}))
    password = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'style':'border: 1px solid #dddfe2;','placeholder':'Password:'}))
    class Meta:
        model = User
        fields = ('username','password')

#register form
class registerForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username:'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First name:'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last name:'}))
    email = forms.EmailField(max_length=258,widget=forms.EmailInput(attrs={'placeholder':'Email:'}))
    password1 = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password:'}))
    password2 = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password:'}))
    class Meta:
        model= User
        fields = ('username','first_name','last_name','email','password1','password2')
#roomBuilding
class roomBuilding(forms.ModelForm):
    buildingRoom = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Building and room'}))
    class Meta:
        model = RoomServer
        fields =['buildingRoom']

class ProfilePicForm(forms.ModelForm):
    
    class Meta:
        model = ProfileUser
        fields = '__all__'
        exclude = ['user']
