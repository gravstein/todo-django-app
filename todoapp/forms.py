from django import forms
from .models import Tasks
from crispy_forms.helper import FormHelper

from django.contrib.auth.models import User

class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Read a book', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False  # Это уберет все лейблы
        self.helper.form_tag = False  # ВАЖНО: говорим не создавать <form>

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        # Check if the passwords match
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data