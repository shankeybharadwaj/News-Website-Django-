from django.shortcuts import render, get_object_or_404, redirect
from .models import ContactForm
from news.models import News
from main.models import Main
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage     # for uploading facility
from contactform.models import ContactForm
import datetime


def contact_add(request):

    site = Main.objects.get(pk=2)   # alt. method
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popular = News.objects.all().order_by('-show')
    popular3 = News.objects.all().order_by('-show')[:3]


    now = datetime.datetime.now()
    year=now.year
    month=now.month
    day=now.day
    hour=now.hour
    minute=now.minute
    if len(str(day))==1:
        day='0'+str(day)
    if len(str(month))==1:
        month='0'+str(month)
    if len(str(hour))==1:
        hour='0'+str(hour)
    if len(str(minute))==1:
        minute='0'+str(minute)
    today = str(year)+'/'+str(month)+'/'+str(day)
    time = str(hour)+':'+str(minute)


    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        txt = request.POST.get('msg')

        if name == '' or email == '' or txt =='':
            msg = 'All Fields Required'
            return render(request, 'front/msgbox.html',{'msg':msg,'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popular':popular,'popular3':popular3})
        
        b = ContactForm(name=name,email=email,txt=txt,date=today,time=time)
        b.save()
        msg = 'Your message has been sent. Thanks for interacting with us.'
        return render(request, 'front/msgbox.html',{'msg':msg,'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popular':popular,'popular3':popular3})

    return render(request,'front/msgbox.html')


def contact_show(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end


    msg = ContactForm.objects.all()

    return render(request, 'back/contact_form.html',{'msg':msg})


def contact_delete(request,pk):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    b = ContactForm.objects.filter(pk=pk)
    b.delete()

    return redirect('contact_show')
