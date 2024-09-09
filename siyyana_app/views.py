from django.http import HttpResponse
from django.shortcuts import render,redirect
from siyyana_app.models import *
from siyyana_app.forms import *
from django.contrib import messages
from siyyana_app.forms import ServicesAddForm
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from accounts.models import *
# Create your views here.

@login_required(login_url="siyyana_app:login")
def index(request):
    return render(request,'index.html')






def login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username_or_email, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['username'] = username_or_email
            return redirect('siyyana_app:index')
        else:
            messages.error(request, 'Invalid credential..')
            return redirect('siyyana_app:login')
    return render(request, 'login.html')




def admin_logout(request):
    logout(request)
    return redirect("siyyana_app:login")


@login_required(login_url="siyyana_app:login")
def services(request):
    data = Category.objects.all()
    context = {'data':data}
    return render(request,'services.html',context)


@login_required(login_url="siyyana_app:login")
def add_services(request):
    if request.method == 'POST':
        form = ServicesAddForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Service added successfully')
            return redirect('siyyana_app:services')
    else:
        form = ServicesAddForm()
    context = {'form':form}
    return render(request,'add-services.html',context)

@login_required(login_url="siyyana_app:login")
def edit_services(request,id):
    update = Category.objects.get(id=id)
    form = ServicesAddForm(instance=update)
    if request.method == 'POST':
        form = ServicesAddForm(request.POST,request.FILES,instance=update)
        if form.is_valid():
            form.save()
            messages.success(request,'Service added successfully')
            return redirect('siyyana_app:services')
    context = {'form':form}
    return render(request,'add-services.html',context)



@login_required(login_url="siyyana_app:login")
def delete_services(request,id):
    delete = Category.objects.get(id=id)
    delete.delete()
    return redirect('siyyana_app:services')




@login_required(login_url="siyyana_app:login")
def sub_services(request):
    data = SubCategory.objects.all().order_by('-id')
    context = {'data':data}
    return render(request,'subservices.html',context)


@login_required(login_url="siyyana_app:login")
def add_subservices(request):
    if request.method == 'POST':
        form = SubServicesAddForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'SubService added successfully')
            return redirect('siyyana_app:sub_services')
    else:
        form = SubServicesAddForm()
    context = {'form':form}
    return render(request,'add-sub-services.html',context)


@login_required(login_url="siyyana_app:login")
def edit_subservices(request,id):
    update = SubCategory.objects.get(id=id)
    form = SubServicesAddForm(instance=update)
    if request.method == 'POST':
        form = SubServicesAddForm(request.POST,request.FILES,instance=update)
        if form.is_valid():
            form.save()
            messages.success(request,'SubService added successfully')
            return redirect('siyyana_app:sub_services')
    context = {'form':form}
    return render(request,'add-sub-services.html',context)


@login_required(login_url="siyyana_app:login")
def delete_subservices(request,id):
    delete = SubCategory.objects.get(id=id)
    delete.delete()
    return redirect('siyyana_app:sub_services')



@login_required(login_url="siyyana_app:login")
def top_services(request):
    data = TopCategory.objects.all().order_by('-id')
    context = {'data':data}
    return render(request,'top-services.html',context)


@login_required(login_url="siyyana_app:login")
def add_topservices(request):
    if request.method == 'POST':
        form = TopServicesAddForm(request.POST,request.FILES)
        category_id  = request.POST.get('Category')
        if TopCategory.objects.filter(Category__id=category_id).exists():
            messages.error(request,'Already Exists')
            return redirect('siyyana_app:top_services')
        if form.is_valid():
            form.save()
            messages.success(request,'added successfully')
            return redirect('siyyana_app:top_services')
    else:
        form = TopServicesAddForm()
    context = {'form':form}
    return render(request,'add-top-services.html',context)

@login_required(login_url="siyyana_app:login")
def edit_topservices(request,id):
    update = TopCategory.objects.get(id=id)
    form = TopServicesAddForm(instance=update)
    if request.method == 'POST':
        form = TopServicesAddForm(request.POST,request.FILES,instance=update)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated successfully')
            return redirect('siyyana_app:top_services')
    context = {'form':form}
    return render(request,'add-top-services.html',context)



@login_required(login_url="siyyana_app:login")
def delete_topservices(request,id):
    delete = TopCategory.objects.get(id=id)
    delete.delete()
    return redirect('siyyana_app:top_services')





@login_required(login_url="siyyana_app:login")
def employee_list(request):
    data = CustomUser.objects.filter(user_type='Employee').order_by('-id')
    context = {'users':data}
    return render(request,'employee.html',context)


@login_required(login_url="siyyana_app:login")
def employee_delete(request,id):
    data = CustomUser.objects.get(id=id)
    data.delete()
    messages.success(request,'Deleted successfully')
    return redirect('siyyana_app:employee_list')



@login_required(login_url="siyyana_app:login")
def user_list(request):
    data = CustomUser.objects.filter(user_type='User').order_by('-id')
    context = {'users':data}
    return render(request,'users.html',context)


@login_required(login_url="siyyana_app:login")
def user_delete(request,id):
    data = CustomUser.objects.get(id=id)
    data.delete()
    messages.success(request,'Deleted successfully')
    return redirect('siyyana_app:user_list')
