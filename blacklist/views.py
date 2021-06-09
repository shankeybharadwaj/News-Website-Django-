from django.shortcuts import render, get_object_or_404, redirect
from .models import BlackList


# Create your views here.


def black_list(request):

    ip_list = BlackList.objects.all()

    return render(request, 'back/blacklist.html', {'ip_list':ip_list})


def ip_add(request):

    if request.method == 'POST':

        ip = request.POST.get('ip')

        if ip != "" :

            b = BlackList(ip=ip)
            b.save()


    return redirect('black_list')


def ip_del(request,pk):
    
    b = BlackList.objects.filter(pk=pk)
    b.delete()

    return redirect('black_list')
