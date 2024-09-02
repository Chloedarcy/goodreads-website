# myapp/forms.py
from django import forms

class GoodreadsLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

