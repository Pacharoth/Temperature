from django import forms
from adminpage.models import userProfile,RoomServer
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from adminpage.utils import weekList
from django.core.exceptions import ValidationError
#login form
class loginForm(forms.Form):
    email = forms.CharField(min_length=8,widget=forms.EmailInput(attrs={'style':'border: 1px solid #dddfe2;','placeholder':'Email:'}))
    password = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'style':'border: 1px solid #dddfe2;','placeholder':'Password:'}))


#register form
class registerForm(UserCreationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Username:'}),label="")
    email = forms.EmailField(required=True,max_length=258,widget=forms.EmailInput(attrs={'placeholder':'Email:'}),label="")
    password1 = forms.CharField(required=True,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password:'}),label="")
    password2 = forms.CharField(required=True,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password:'}),label="")

    def clean_email(self):
        email= self.cleaned_data.get("email")
        emailObj = User.objects.filter(email=email)
        if emailObj.exists():
            raise forms.ValidationError(_("Email already exists"))
        return email
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)
    class Meta:
        model= User
        fields = ['username','email','password1','password2']
#change password form in user
class resetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New password','autocomplete': 'new-password'}))
    new_password2 = forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password','autocomplete': 'new-password'}))
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


#roomBuilding
class roomBuildingForm(forms.ModelForm):
    buildingRoom = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Building and room','class':'form-control'}))
    def clean_room(self):
        room = self.cleaned_data.get('buildingRoom')
        roomObj = RoomServer.objects.filter(buildingRoom=room)
        if roomObj.exists():
            raise forms.ValidationError(_("Room already has owner"))
        return room
    class Meta:
        model = RoomServer
        fields =['buildingRoom']
        
#roomedit form
class roomEdit(forms.ModelForm):
    building = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = RoomServer
        fields=['buildingRoom']

#profile pic
class ProfilePic(forms.ModelForm):
    phone= forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number:'}))
    # img = forms.ImageField(max_length=5,widget=forms.FileInput(attrs={'class':'form-control'}))
    def clean_phone(self):
        phonenumber = self.cleaned_data.get('phone')
        if phonenumber is None or phonenumber == "":
            raise forms.ValidationError(_("Please insert phone number and pic"))
        return phonenumber
    
    class Meta:
        model = userProfile
        fields = ['phone','img']


#profile usernamed
class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username:'}))
    class Meta:
        model = User
        fields = ['username']

#form for the generate report 
WEEK=[(1,"Week1"),(2,"Week2"),(3,"Week3"),(4,"Week4")]  
YEAR_VALID=[(data,data) for data in range(2012,3000)]
MONTH_VALID=[(1,'Jan'),
            (2,'Feb'),
            (3,'Mar'),
            (4,'Apr'),
            (5,'May'),
            (6,'June'),
            (7,'July'),
            (8,'Aug'),
            (9,'Sep'),
            (10,'Oct'),
            (11,'Nov'),
            (12,'Dec')]
class choiceForm_weekly(forms.Form):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    week_form=forms.ChoiceField(widget=forms.Select(attrs={'class':'custom-select mr-sm-2'}),choices=WEEK)
    month_form = forms.ChoiceField(required=True,widget=forms.Select(attrs={'class':'custom-select mr-sm-2'}),choices=MONTH_VALID)
    year_form= forms.ChoiceField(required=True,widget=forms.Select(attrs={'class':'custom-select mr-sm-2'}),choices=YEAR_VALID)
    def cleanform(self,room):
        week= self.cleaned_data.get("week_form")
        month=self.cleaned_data.get("month_form")
        year=self.cleaned_data.get("year_form")
        dataweek,avg= weekList(room,int(week),int(month),int(year))
        return dataweek,avg,week,month,year
class choiceForm_monthly(forms.Form):
    month_form = forms.ChoiceField(required=True,widget=forms.Select(attrs={'class':' custom-select mr-sm-2'}),choices=MONTH_VALID)
    year_form = forms.ChoiceField(required=True,widget=forms.Select(attrs={'class':'custom-select mr-sm-2'}),choices=YEAR_VALID)

class choiceForm_annually(forms.Form):
    year_form = forms.ChoiceField(required=True,widget=forms.Select(attrs={'class':'custom-select mr-sm-2'}),choices=YEAR_VALID)