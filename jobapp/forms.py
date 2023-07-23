from django import forms
from .views import *

class applicantform(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    birthday = forms.DateField()
    phone = forms.IntegerField()
    highest_qualification = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20)
    confirm_password = forms.CharField(max_length=20)

class user_logform(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=20)

class adminform(forms.Form):
    uname=forms.CharField(max_length=20)
    password=forms.CharField(max_length=20)

# send message

class MessageForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows':3,'cols':40}))


class contactform(forms.Form):
    name=forms.CharField(max_length=20)
    email=forms.EmailField()
    message=forms.CharField(max_length=500,widget=forms.Textarea(attrs={'row':3,'col':30}))

# Create the form class.
class jobaddform(forms.Form):
    company_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=254)
    job_title = forms.CharField(max_length=20)
    work_type = forms.CharField(max_length=20)
    experience = forms.CharField(max_length=20)
    job_type = forms.CharField(max_length=20)

