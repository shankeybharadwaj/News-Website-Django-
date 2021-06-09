from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from manager.models import Manager
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage     # for uploading facility
from django.contrib.auth.models import User, Group, Permission
import string
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from blacklist.models import BlackList

# Create your views here.

def home(request):

    # site = Main.objects.filter(pk=2)       # For this, for loop required(query) in master to show title # site = Main.objects.all()  
    site = Main.objects.get(pk=2)   # alt. method
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popular = News.objects.filter(act=1).order_by('-show')
    popular3 = News.objects.filter(act=1).order_by('-show')[:3]

    return render(request,'front/home.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popular':popular,'popular3':popular3})


def about(request):

    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popular = News.objects.all().order_by('-show')
    popular3 = News.objects.all().order_by('-show')[:3]
    return render(request,'front/about.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popular':popular,'popular3':popular3})

def contact(request):

    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popular = News.objects.all().order_by('-show')
    popular3 = News.objects.all().order_by('-show')[:3]
    return render(request,'front/contact.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popular':popular,'popular3':popular3})


def panel(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm=0
    perms = Permission.objects.filter(user=request.user)
    for i in perms:
        if i.codename == 'master_user':
            perm=1
    
    # if perm == 0:
    #     error = 'Access Denied!!!'
    #     return render(request, 'back/error.html',{'error':error})

    return render(request, 'back/home.html')



def mylogin(request):

    if request.method == 'POST':
        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "" :
            user1 = authenticate(username=utxt, password=ptxt)  # if credentials incorrect, returns None to user1

            if user1 != None :

                ip, is_routable = get_client_ip(request)

                if ip is None :

                    ip = "0.0.0.0"

                b = len(BlackList.objects.filter(ip=ip))

                if b != 0 :
                    msg = "Your ip Blocked By Admin"
                    return render(request, 'front/msgbox.html', {'msg':msg})

                login(request,user1)
                return redirect('panel')

    return render(request, 'front/login.html')


def mylogout(request):

    logout(request)

    return redirect('mylogin')


def myregister(request):

    site = Main.objects.get(pk=2)

    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if name == '':
            msg = "Please enter your name..."
            return render(request,'front/msgbox.html',{'msg':msg,'site':site})

        if password1 != password2:
            msg = "The entered passwords are different!!"
            return render(request,'front/msgbox.html',{'msg':msg,'site':site})
        
        if len(password1)<8:
                msg = 'Password must contain atleast 8 characters.'
                return render(request,'front/msgbox.html',{'msg':msg,'site':site})

        c1,ca,cA=0,0,0

        for ch in password1:
            if ch in string.digits:
                c1=1
            if ch in string.ascii_lowercase:
                ca=1
            if ch in string.ascii_uppercase:
                cA=1
            
        if c1==0 or ca==0 or cA==0:
            msg = 'Password too weak!! Please enter a strong password.'
            return render(request,'front/msgbox.html',{'msg':msg,'site':site})

        
        if len(User.objects.filter(username=uname))==0 and len(User.objects.filter(password=password1))==0:
            
            ip, is_routable = get_client_ip(request)

            if ip is None :

                ip = "0.0.0.0"

            try :

                response = DbIpCity.get(ip,api_key='free')
                country = response.country + " | " + response.city

            except:

                country = "Unknown"

            user = User.objects.create_user(username=uname,email=email,password=password1)
            b = Manager(name=name,utxt=uname,email=email,ip=ip,country=country)
            b.save()
        

    return render(request, 'front/login.html')


def site_setting(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1
    if perm == 0:
        error = 'Access Denied!!!'
        return render(request, 'back/error.html',{'error':error})

    if request.method=="POST":
        name = request.POST.get("name")
        fb = request.POST.get("fb")
        tw = request.POST.get("tw")
        yt = request.POST.get("yt")
        tell = request.POST.get("tell")
        link = request.POST.get("link")
        txt = request.POST.get("txt")

        if fb=='':fb='#'
        if tw=='':tw='#'
        if yt=='':yt='#'
        if link=='':link='#'

        if name=='' or tell=='' or txt=='':
            error = 'All Fields Required'
            return render(request, 'back/error.html',{'error':error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()    # making object
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            b = Main.objects.get(pk=2)
            b.name=name
            b.fb=fb
            b.tw=tw
            b.yt=yt
            b.tell=tell
            b.about=txt
            b.link=link
            b.picurl=url
            b.picname=filename

            b.save()
        except:
            b = Main.objects.get(pk=2)
            b.name=name
            b.fb=fb
            b.tw=tw
            b.yt=yt
            b.tell=tell
            b.about=txt
            b.link=link
            
            b.save()

        

    site = Main.objects.get(pk=2)

    return render(request,'back/setting.html',{'site':site})


def about_setting(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1
    if perm == 0:
        error = 'Access Denied!!!'
        return render(request, 'back/error.html',{'error':error})

    about1 = Main.objects.get(pk=2).abouttxt

    if request.method == 'POST':
        txt = request.POST.get('abouttxt')
        if txt == '':
            error = 'All Fields Required'
            return render(request, 'back/error.html',{'error':error}) 
        about2 = Main.objects.get(pk=2)
        about2.abouttxt = txt
        about2.save()
        return redirect('about')

    return render(request,'back/about_setting.html',{'about1':about1})


def change_pass(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if request.method == 'POST':
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass=='' or newpass=='':
            error = 'All Fields Required'
            return render(request, 'back/error.html',{'error':error})
        
        user1 = authenticate(username=request.user,password=oldpass)
        if user1 != None:

            if len(newpass)<8:
                error = 'Password must contain atleast 8 characters.'
                return render(request, 'back/error.html',{'error':error})

            c1,ca,cA=0,0,0

            for ch in newpass:
                if ch in string.digits:
                    c1=1
                if ch in string.ascii_lowercase:
                    ca=1
                if ch in string.ascii_uppercase:
                    cA=1
                
            if c1==1 and ca==1 and cA==1:
                user1 = User.objects.get(username=request.user)
                user1.set_password(newpass)
                user1.save()
                return redirect('mylogout')
            else:
                error = 'Password too weak!! Please enter a strong password. '
                return render(request, 'back/error.html',{'error':error})
            
            
        else:
            error = 'OOPS! Your old password does not match.'
            return render(request, 'back/error.html',{'error':error})
        


    return render(request,'back/changepass.html')