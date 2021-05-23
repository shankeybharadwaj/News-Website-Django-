from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage     # for uploading facility
import datetime
from subcat.models import SubCat
from cat.models import Cat


# Create your views here.

def news_detail(request,pk):    # (request,word)

    site = Main.objects.get(pk=2)
    news1 = News.objects.filter(pk=pk)   # News.objects.filter(name = word) 
    site = Main.objects.get(pk=2)   # alt. method
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popular = News.objects.all().order_by('-show')
    popular3 = News.objects.all().order_by('-show')[:3]
    tag = News.objects.get(pk=pk).tag.split(',')

    mynews = News.objects.get(pk=pk)
    mynews.show +=1
    mynews.save()

    return render(request,'front/news_detail.html',{'news1':news1,'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popular':popular,'popular3':popular3,'tag':tag})


def news_list(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1
    
    if perm == 0:
        news = News.objects.filter(writer=request.user)
    elif perm == 1:
        news = News.objects.all()
    

    return render(request, 'back/news_list.html',{'news':news})

def news_add(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

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

    subcat = SubCat.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newsid = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        tag = request.POST.get('tag')
        

        if newstitle == "" or newstxt == "" or newstxtshort == "" or newsid == "":
            error = 'All Fields Required'
            return render(request, 'back/error.html',{'error':error})
        
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()    # making object
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):
                if myfile.size >5000000:
                    fs=FileSystemStorage()
                    fs.delete(filename)
                    error = 'Your file size is more than 5 MB.'
                    return render(request, 'back/error.html',{'error':error})

                cat_name = SubCat.objects.get(pk=newsid).catname+' | '+ SubCat.objects.get(pk=newsid).name
                ocatid = SubCat.objects.get(pk=newsid).catid

                b = News(name=newstitle , short_txt=newstxtshort , body_txt=newstxt , date=today ,time=time, picurl=url, picname=filename,  writer=request.user, catname=cat_name , catid=newsid , ocatid=ocatid , show=0,tag=tag)
                b.save()

                count = len(News.objects.filter(ocatid=ocatid))
                b = Cat.objects.get(pk=ocatid)
                b.count = count
                b.save()

                return redirect('news_list')    # news_list  function
            else:
                fs=FileSystemStorage()
                fs.delete(filename)

                error = 'File format not supported. Please upload an image.'
                return render(request, 'back/error.html',{'error':error})

        except:
            error = 'OOPS!! You forgot to upload the image.'
            return render(request, 'back/error.html',{'error':error})

    return render(request, 'back/news_add.html',{'subcat':subcat})



def news_delete(request,pk):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1
    
    if perm == 0:
        aa = News.objects.get(pk=pk).writer
        if aa != request.user.username:
            error = 'Access Denied!!!'
            return render(request, 'back/error.html',{'error':error})

    try:
        item = News.objects.get(pk=pk)

        fs=FileSystemStorage()
        fs.delete(item.picname)

        ocatid = News.objects.get(pk=pk).ocatid

        item.delete()

        
        count = len(News.objects.filter(ocatid=ocatid))
        b = Cat.objects.get(pk=ocatid)
        b.count = count
        b.save()


    except:
        error = 'Something Wrong!!'
        return render(request, 'back/error.html',{'error':error})

    return redirect('news_list')



def news_publish(request,pk):

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

    this_news = News.objects.get(pk=pk)
    if this_news.act == 0:
        this_news.act = 1
    else:
        this_news.act = 0
    this_news.save()

    return redirect('news_list')


def news_edit(request,pk):

    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if len(News.objects.filter(pk=pk)) == 0:
        error = 'News not found!!'
        return render(request, 'back/error.html',{'error':error})

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1
    
    if perm == 0:
        aa = News.objects.get(pk=pk).writer
        if aa != request.user.username:
            error = 'Access Denied!!!'
            return render(request, 'back/error.html',{'error':error})

    

    news = News.objects.get(pk=pk)
    subcat = SubCat.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newsid = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        tag = request.POST.get('tag')

        if newstitle == "" or newstxt == "" or newstxtshort == "" or newsid == "":
            error = 'All Fields Required'
            return render(request, 'back/error.html',{'error':error})
        
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()    # making object
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):
                if myfile.size >5000000:
                    fs=FileSystemStorage()
                    fs.delete(filename)
                    error = 'Your file size is more than 5 MB.'
                    return render(request, 'back/error.html',{'error':error})

                cat_name = SubCat.objects.get(pk=newsid).catname+' | '+SubCat.objects.get(pk=newsid).name

                b = News.objects.get(pk=pk)
                

                fss=FileSystemStorage()  # delete old image
                fss.delete(b.picname)

                b.name=newstitle    # overwriting
                b.catname=cat_name
                b.catid=newsid
                b.short_txt=newstxtshort
                b.body_txt=newstxt
                b.picurl=url
                b.picname=filename
                b.tag=tag
                b.act=0

                b.save()
                return redirect('news_list')    # news_list  function
            else:
                fs=FileSystemStorage()
                fs.delete(filename)

                error = 'File format not supported. Please upload an image.'
                return render(request, 'back/error.html',{'error':error})

        except:
            # here if if image not uploaded while editting
            cat_name = SubCat.objects.get(pk=newsid).catname+' | '+ SubCat.objects.get(pk=newsid).name

            b = News.objects.get(pk=pk)

            b.name=newstitle    
            b.catname=cat_name
            b.catid=newsid
            b.short_txt=newstxtshort
            b.body_txt=newstxt
            b.tag=tag
            b.act=0

            b.save()
            return redirect('news_list')    # news_list  function

    return render(request, 'back/news_edit.html',{'pk':pk,'subcat':subcat,'news':news})