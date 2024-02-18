from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Custom_User
        fields = UserCreationForm.Meta.fields + ('display_name', 'email','city', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].help_text = None

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Custom_User  
        fields = ['username', 'password']

class userProfileForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields= ('__all__')
        exclude=['user', 'BMR']


class itemsallForm(forms.ModelForm):

    class Meta:
        model = itemsall
        fields= ('__all__')
        exclude=['user']


class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    date = forms.DateField(
        widget=DateInput(attrs={'placeholder': 'YYYY-MM-DD'})
    )
