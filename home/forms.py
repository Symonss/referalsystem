from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Prospect


class Admin_uSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
        return user


class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'phone', 'password1', 'password2', )

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_user = True
        if commit:
            user.save()
        return user


class NewProspectForm(forms.ModelForm):
    class Meta:
        model = Prospect
        fields = ['full_name', 'phone']
