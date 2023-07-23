
from django.db import models
from django.contrib.auth.models import User


class jobseeker(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    birthday = models.DateField()
    phone = models.IntegerField()
    highest_qualification = models.CharField(max_length=50)
    password = models.CharField(max_length=20)



class Message(models.Model):
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

class companyprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=20)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)



class addjob(models.Model): # company details
    company_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)  # Use EmailField for email addresses
    job_title = models.CharField(max_length=20)

    WORK_TYPES = [
        ("hybrid", "hybrid"),
        ("rural", "rural"),
        ("city", "city"),
    ]
    work_type = models.CharField(max_length=20, choices=WORK_TYPES)

    experience = models.CharField(max_length=20)
    job_type = models.CharField(max_length=20)

class applied(models.Model): # jobseeker application details
    company_name=models.CharField(max_length=20)
    designation=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    email=models.EmailField()
    qualification=models.CharField(max_length=20)
    phone_num=models.IntegerField()
    experience=models.CharField(max_length=20)
    upload_resume=models.ImageField(upload_to='jobapp/static')





