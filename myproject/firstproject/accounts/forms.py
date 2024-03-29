from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=300, required=True,
                            widget=forms.EmailInput(), help_text="email like example@gmail.com")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
