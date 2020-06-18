from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2", )

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
