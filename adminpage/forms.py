from django import forms
from django.contrib.auth.models import User


#login form
class loginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'style':'border: 1px solid #dddfe2;','placeholder':'Username'}))
    password = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'style':'border: 1px solid #dddfe2;','placeholder':'Password:'}))
    class Meta:
        model = User
        fields = ('username','password')