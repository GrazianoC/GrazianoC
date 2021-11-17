from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


#in questo modo estendo la classe UserCreationForm quindi posso assegnare la form SignUpForm
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.') #includo il 
    CHOICES=[('1','Donatore'),
             ('2','Associazione')]
    groups = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ["username", "first_name", "email", "groups", "password1", "password2"]


