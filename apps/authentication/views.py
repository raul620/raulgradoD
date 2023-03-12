# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm,ProfileSettings
from django.contrib.auth.models import Group

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get("myRole"))
            role = form.cleaned_data.get("myRole")
            group = Group.objects.get(name=role)
 
            user=form.save()
            user.groups.add(group)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def profile_settings(request):
    print("AAAAAAAAAAAA")
    msg = None
    success = False
    user =request.user
    form = ProfileSettings(instance=user)
    print("form",form)
    context= {'form':form}

    if request.method == "POST":
        form = ProfileSettings(request.POST,request.FILES or None,instance=user)
        context= {'form':form}
        if form.is_valid():
            
            form.save()
            #username = form.cleaned_data.get("username")
            #raw_password = form.cleaned_data.get("password1")
            #user = authenticate(username=username, password=raw_password)

            msg = 'User updated successfully.'
            success = True
            return render(request, "home/user.html", context)

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = ProfileSettings()

    return render(request, "home/user.html", context)