from django.contrib.auth.forms import UserCreationForm
from django import forms

from oss_main.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        )


class ProfileForm(forms.Form):
    pass
    # class Meta:
    #     model = User
    #     fields = ['username', 'first_name', 'last_name', 'git_url']