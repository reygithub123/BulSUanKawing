from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import CreateUserForm, InitializeOrgForm
from organization.models import Organization 
from django.contrib import messages


def view_login(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.POST.get('next')
            org = Organization.objects.filter(user__id=user.id).first()
            if org.state=="s":
                return redirect('org:view-account-setup')
            if request.user.is_superuser:
                return redirect(f'/cms/')
            elif request.POST.get('next'):
                return redirect (next)
            else:
                return redirect(f'/user/')
        else:
            messages.info(request, "Username OR Password is incorrect")
            return render(request, 'login.html', {})
    return render(request, 'login.html', {})

@login_required
def view_logout(request):
    logout(request)
    return redirect('/')
    
def view_signup(request, *args, **kwargs):
   
    
    if request.method == 'POST':
        accform = CreateUserForm(request.POST)
        orgform = InitializeOrgForm(request.POST)
        if accform.is_valid():
            accform.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            loginuser = authenticate(request, username=username, password=password)
            login(request, loginuser)
            currentuser = request.user
            org = Organization.objects.create(user=currentuser,name=currentuser.username,state='s')
            return redirect("org:view-account-setup")
            
    else: 
        data = {'user':None,'state':'s'}
        accform = CreateUserForm()
        orgform = InitializeOrgForm(initial=data)

    context = {
        
        'form': accform,
        'orgform': orgform,
               }

    return render(request, 'registration.html', context)

