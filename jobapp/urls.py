from django.urls import path
from .views import *
# from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',indexview,name="index"),
    path('jobseeker-login/',jobseeker_log),
    path('register/',jobseeker_reg),
    path('log/',adminlogin),
    path('edit_applicant/<int:id>/', edit_applicant),
    path('pro/',adminpro),
    path('adminpro/',admindisp),
    
    #admin urls
    path('reg/', regis),
    path('success/',success),
    path('send/',send_mail_regis),
    path('verify/<auth_token>',verify),
    
    # send message
    path('message/', send_message, name='send_message'),
    path('list/',listcompanies),
    path('addjob/',addjob1),
    path('listjobs/<int:id>/',listjobs),
    path('apply/<int:id1>/<int:id2>',applyjob),
    path('applicants/<int:id>',applicantview),
    path('listapplied/<int:id>', jobseeker_applied_jobs),
]
