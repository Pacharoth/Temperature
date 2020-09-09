from django import forms
from adminpage.models import RoomServer,userProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#login form
class loginForm(forms.Form):
    email = forms.CharField(min_length=8,widget=forms.EmailInput(attrs={'style':'border: 1px solid #dddfe2;','placeholder':'Email:'}))
    password = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'style':'border: 1px solid #dddfe2;','placeholder':'Password:'}))
#register form
class registerForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username:'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First name:'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last name:'}))
    email = forms.EmailField(max_length=258,widget=forms.EmailInput(attrs={'placeholder':'Email:'}))
    password1 = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password:'}))
    password2 = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password:'}))
    class Meta:
        model= User
        fields = "__all__"
#roomBuilding
class roomBuilding(forms.ModelForm):
    buildingRoom = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Building and room'}))
    class Meta:
        model = RoomServer
        fields =['buildingRoom']

#profile pic
class ProfilePic(forms.ModelForm):
    phone= forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number:'}))
    img = forms.ImageField(max_length=5,widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = userProfile
        fields = '__all__'
        exclude=['user']

#profile usernamed
class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username:'}))
    class Meta:
        model = User
        fields = "__all__"
        exclude = ['email','first_name','last_name','password1','password2']
