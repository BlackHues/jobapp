# imported here to access
from django.shortcuts import render,redirect,HttpResponse
from .forms import *
from .models import *
from .forms import applicantform,jobaddform,contactform,user_logform
from djangoproject.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate
import uuid
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# views

def indexview(request): 
    return render(request,"index.html") # opens index.html

def jobseeker_reg(request): # registration
        if request.method == 'POST': # validation for registration
            a = applicantform(request.POST)
            if a.is_valid():
                nm = a.cleaned_data['name']
                eml = a.cleaned_data['email']
                br = a.cleaned_data['birthday']
                ph = a.cleaned_data['phone']
                hq = a.cleaned_data['highest_qualification']
                pa = a.cleaned_data['password']
                cpa = a.cleaned_data['confirm_password']
                if pa == cpa:
                    b = jobseeker(name=nm,email=eml,birthday=br,phone=ph,highest_qualification=hq,password=pa) # stored in db (models)
                    b.save() # saved
                    return redirect(jobseeker_log) # redirect to login page
                else:
                    return HttpResponse("Incorrect password.....")
            else:
                return HttpResponse("Enter valid data")
        return render(request,'jobseeker_register.html') # jobseeker registration page
#
#
#
#
#
def jobseeker_log(request):
    if request.method == 'POST':
        user = user_logform(request.POST)

        if user.is_valid():
            eml = user.cleaned_data['email']
            pas = user.cleaned_data['password']

            x = jobseeker.objects.all()
            for i in x:
                if eml == i.email and pas == i.password:
                    nm=i.name
                    em=i.email
                    br=i.birthday
                    ph=i.phone
                    hq=i.highest_qualification
                    id1=i.id
                    return render(request,'jobHomepage.html',{'name':nm,'email':em,'birthday':br,'phone':ph,'highest_qualification':hq,'id':id1})
            else:
                return HttpResponse("password incorrect...")
        else:
            return HttpResponse("error...")
    return render(request,'jobseeker_login.html') # jobseeker login
#
# jobseeker details displayed in offcanvas
def edit_applicant(request, id):
    applicant = jobseeker.objects.get(id=id) # to get one by one relation

    if request.method == 'POST':
        applicant.name = request.POST.get('name')
        applicant.email = request.POST.get('email')
        applicant.birthday = request.POST.get('birthday')
        applicant.phone = request.POST.get('phone')
        applicant.highest_qualification = request.POST.get('highest_qualification')
        applicant.password = request.POST.get('password')
        applicant.save()
        return redirect(jobseeker_log)  # Redirect to a page showing the list of all applicants

    return render(request, 'jobseeker_edit.html', {'applicant': applicant})
#
#
# # admin login
def adminpro(request):
    return render(request,'admin_register.html')

# admin profile
def admindisp(request):
    return render(request,'adminprofile.html')



def adminlogin(request):
            global User;
            if request.method=='POST':
                username=request.POST.get('uname')
                pas=request.POST.get('password')
                user_obj=User.objects.filter(username=username).first()
                if user_obj is None:
                    messages.success(request,'user not found')
                    return redirect(adminlogin)
                profile_obj=companyprofile.objects.filter(user=user_obj).first()
                if not profile_obj.is_verified:
                    messages.success(request,'profile not verified check your email')
                    return redirect(adminlogin)
                User=authenticate(username=username,password=pas)

                if User is None:
                    messages.success(request,'wrong password no such username')
                    return redirect(adminlogin)

                obj=companyprofile.objects.filter(user=User)
                return render(request,"adminprofile.html",{"obj":obj})
            return render(request,'admin_login.html')



def verify(request, auth_token):
    try:
        profile_obj = companyprofile.objects.get(auth_token=auth_token)
    except ObjectDoesNotExist:
        return HttpResponse('Error: Invalid authentication token')

    if profile_obj.is_verified:
        messages.success(request, 'Your account is already verified')
    else:
        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request, 'Your account has been verified')

    return redirect(adminlogin)


def regis(request):
    if request.method == 'POST':
        username=request.POST.get('uname')
        email=request.POST.get('email')
        pas = request.POST.get('password')
        if  User.objects.filter(username=username).first():
            messages.success(request,"email already taken")
            return redirect(regis)
        if  User.objects.filter(email=email).first():
            messages.success(request,"email already taken")
            return redirect(regis)
        user_obj=User(username=username,email=email)
        user_obj.set_password(pas)
        user_obj.save()
        auth_token=str(uuid.uuid4())
        profile_obj=companyprofile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_mail_regis(email,auth_token)
        return redirect(success)
    return render(request,"admin_register.html")

def send_mail_regis(email,token):
    subject="your account has been verified"
    message=f'pass the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)

def success(request):
    return render(request,"success.html")



def send_message(request):
    sub=contactform()
    if request.method=='POST':
        sub=contactform(request.POST)
        if sub.is_valid():
            name=sub.cleaned_data['name']
            message=sub.cleaned_data['message']
            email=sub.cleaned_data['email']
            send_mail((str(name))+'||'+ str(message),email,EMAIL_HOST_USER,[email],fail_silently=False)
            # subject+fromemail+recipientemail+message

            return render(request,'success.html')
    return render(request,'message_form.html',{'form':sub})


def listcompanies(request):
    company_profiles = companyprofile.objects.all()
    comp = []
    email = []
    id1 = []

    for profile in company_profiles:
        c = profile.user.username
        comp.append(c)
        e = profile.user.email
        email.append(e)
        k = profile.user.id
        id1.append(k)

    mylist = zip(comp, email, id1)
    return render(request, 'listCompanies.html', {"mylist": mylist})

def addjob1(request):
    if request.method == "GET":
        return render(request,'admin_addjob.html')

    elif request.method == "POST":
        a=jobaddform(request.POST)
        if a.is_valid():
            nm = a.cleaned_data['company_name']
            em = a.cleaned_data["email"]
            jb=a.cleaned_data["job_title"]
            jt = a.cleaned_data['job_type']
            wt = a.cleaned_data['work_type']
            ep = a.cleaned_data['experience']
            b = addjob(company_name=nm,email=em,job_title=jb,job_type=jt,work_type=wt,experience=ep)
            b.save()
            return HttpResponse('success')
        else:
            return HttpResponse('error')
    return render(request,'list_jobs.html')

# views.py

def listjobs(request,id):
    jobs = addjob.objects.all()
    userid=id
    comp = []
    email = []
    jb=[]
    jt=[]
    wt=[]
    ep=[]
    id1 = []

    for i in jobs:
        com = i.company_name
        comp.append(com)

        a = i.id
        id1.append(a)

        em=i.email
        email.append(em)

        jb1=i.job_title
        jb.append(jb1)

        jt1=i.job_type
        jt.append(jt1)

        wt1=i.work_type
        wt.append(wt1)

        exp=i.experience
        ep.append(exp)

    mylist = zip(jb,comp,email,jt,wt,ep,id1)
    return render(request, 'list_jobs.html', {"jobs": mylist,"userid":userid})

def applyjob(request,id1,id2):
    # id2 for jobseeker_details, id1 for job_details
    # variable = models.objects.get(id=id1)

    user=jobseeker.objects.get(id=id2)
    job=addjob.objects.get(id=id1)

    uname=user.name
    uemail=user.email

    cname=job.company_name
    cjob=job.job_title

    mylist={'a':uname,'b':uemail,'c':cname,'d':cjob}
    if request.method=='POST':
            apply=applied()
            apply.company_name=request.POST.get('company_name')
            apply.designation=request.POST.get('designation')
            apply.name=request.POST.get('name')
            apply.email=request.POST.get('email')
            apply.qualification=request.POST.get('qualification')
            apply.phone_num=request.POST.get('phone_num')
            apply.experience=request.POST.get('experience')
            apply.upload_resume=request.FILES['upload']
            apply.save()

            return render (request,'jobsendsuccess.html')
    return render(request,'applyjob.html',mylist)


def applicantview(request,id): # request and an id parameter
    applicants=applied.objects.all() # retrieves objects from applied model
    jobs=companyprofile.objects.get(id=id) # retrieves single object from companyprofile model on provided id
    comp=jobs.user.username # retrieves username of user associated with the jobs object
    # empty list
    nm=[]
    em=[]
    qn=[]
    pn=[]
    ep=[]
    ur=[]
    # iterated
    for i in applicants:
        if i.company_name==comp:
            nm1=i.name
            nm.append(nm1)
            em1=i.email
            em.append(em1)
            qn1=i.qualification
            qn.append(qn1)
            pn1=i.phone_num
            pn.append(pn1)
            ep1=i.experience
            ep.append(ep1)
            ur1=i.upload_resume
            ur.append(str(ur1).split('/')[-1]) #fileupload
    mylist=zip(nm,em,qn,pn,ep,ur)
    return render (request,'viewapplicant.html',{'mylist':mylist})
def jobseeker_applied_jobs(request, id):
    jobs = applied.objects.all()
    applicants = jobseeker.objects.get(id=id)
    jobseeker_name = applicants.name

    cn = []
    de=[]

    for i in jobs:
        if i.name == jobseeker_name:
            cn1 = i.company_name
            cn.append(cn1)
            de1= i.designation
            de.append(de1)




    mylist=zip(cn,de)
    return render (request,'child.html',{'mylist':mylist})


def child(request):
    return render(request,'base.html')





