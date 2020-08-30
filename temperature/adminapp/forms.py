from django import forms
from adminapp.models import adminControl


#login form
class loginForm(forms.ModelForm):
    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={'placeholder':'Email:','style':'border: 1px solid #dddfe2;'}))
    password = forms.CharField(min_length=8,required=True,widget=forms.PasswordInput(attrs={'placeholder':'Password:','style':'border: 1px solid #dddfe2;'}))
    
    class Meta:
        model=adminControl
        fields = ['email','password']