from django.shortcuts import render, get_object_or_404, redirect
from .models import Manager
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage     # for uploading facility
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
import string

# Create your views here.

def manager_list(request):

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

    managers = Manager.objects.all()
    
    return render(request,'back/manager_list.html',{'managers':managers})


def manager_del(request,pk):

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

    man = Manager.objects.get(pk=pk)
    b = User.objects.filter(username=man.utxt)

    b.delete()
    man.delete()
    
    return redirect('manager_list')


def manager_group(request):

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

    groups = Group.objects.all().exclude(name='masteruser')
    
    return render(request,'back/manager_group.html',{'groups':groups})



def manager_group_add(request):

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


    if request.method == "POST":
        name = request.POST.get('name')

        

        if name != '':
            if len(Group.objects.filter(name=name)) == 0:
                new_grp = Group(name=name)
                new_grp.save()
    
    
    return redirect('manager_group')


def manager_group_del(request,name):

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

    b = Group.objects.filter(name=name)
    b.delete()
    
    return redirect('manager_group')


def user_groups(request,pk):

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

    man = Manager.objects.get(pk=pk)
    this_user = User.objects.get(username=man.utxt)
    this_user_groups = []
    for i in this_user.groups.all():
        this_user_groups.append(i.name)

    groups = Group.objects.all()

    return render(request,'back/user_groups.html',{'this_user_groups':this_user_groups,'groups':groups,'pk':pk})



def add_user_to_group(request,pk):

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

    if request.method == 'POST':
        grp_name = request.POST.get('grp_name')
        grp = Group.objects.get(name=grp_name)
        man = Manager.objects.get(pk=pk)
        user1= User.objects.get(username=man.utxt)
        user1.groups.add(grp)

    return redirect('user_groups', pk=pk)


def del_group_from_user(request,pk,name):

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

    grp = Group.objects.get(name=name)
    man = Manager.objects.get(pk=pk)
    user1= User.objects.get(username=man.utxt)
    user1.groups.remove(grp)

    return redirect('user_groups', pk=pk)



def manager_perms(request):

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

    perms = Permission.objects.all()
    
    return render(request,'back/manager_perms.html',{'perms':perms})


def manager_perms_del(request,name):

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

    perms = Permission.objects.filter(name=name)
    perms.delete()
    
    return redirect('manager_perms')


def manager_perms_add(request):

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

    if request.method == "POST":
        name = request.POST.get('name')
        cname = request.POST.get('cname')

        if len(Permission.objects.filter(codename=cname)) == 0:
            content_type = ContentType.objects.get(app_label='main', model='main')  # providing the app for which the permission is made
            permission = Permission.objects.create(codename=cname, name=name, content_type=content_type)      
        else:
            error = 'This Codename used before!!'
            return render(request, 'back/error.html',{'error':error})
    
    return redirect('manager_perms')




def user_perms(request,pk):

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

    man = Manager.objects.get(pk=pk)
    this_user = User.objects.get(username=man.utxt)

    permission = Permission.objects.filter(user=this_user)

    this_user_perms = []
    for i in permission:
        this_user_perms.append(i.name)

    groups = Group.objects.all()

    perms = Permission.objects.all()

    return render(request,'back/user_perms.html',{'this_user_perms':this_user_perms,'groups':groups,'pk':pk,'perms':perms})




def del_perm_from_user(request,pk,name):

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

    man = Manager.objects.get(pk=pk)
    this_user = User.objects.get(username=man.utxt)

    permission = Permission.objects.get(name=name)
    this_user.user_permissions.remove(permission)

    return redirect('user_perms',pk=pk)



def add_perm_to_user(request,pk):

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

    

    if request.method=='POST':
        man = Manager.objects.get(pk=pk)
        this_user = User.objects.get(username=man.utxt)
        pname=request.POST.get('pname')
        permission = Permission.objects.get(name=pname)
        this_user.user_permissions.add(permission)

    return redirect('user_perms',pk=pk)




def group_perms(request,name):

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

    grp = Group.objects.get(name=name)
    perms = grp.permissions.all()

    allperms = Permission.objects.all()
    

    return render(request,'back/group_perms.html',{'perms':perms,'name':name,'allperms':allperms})




def add_perm_to_group(request,name):

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


    if request.method == 'POST':
        grp = Group.objects.get(name=name)
        pname = request.POST.get('pname')
        perm = Permission.objects.get(name=pname)
        grp.permissions.add(perm)
        

    return redirect('group_perms', name=name)




def del_perm_from_group(request,gname,pname):

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

    
    grp = Group.objects.get(name=gname)
    perm = Permission.objects.get(name=pname)

    grp.permissions.remove(perm)
    

    return redirect('group_perms',name=gname)

