from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt



def index(request):
    return render(request,'main.html')

def new_user(request):
    print("PRINTING POST DATA: ", request.POST)

    #<<--------VALIDATIONS-------->>
    errors = User.objects.basic_validator(request.POST)


    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags='new_user')

        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect(index)
    else:
        
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = request.POST['password'])

        #store user id in session
        request.session['id'] = user.id
        request.session['username']=user.username

        return redirect(dashboard)

def login(request):
    print("LOGIN REQUEST EXECUTED")
    print(request.POST)

    errors = User.objects.login_validator(request.POST)
    print(errors)


    if len(errors)>0:
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login')

        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect(index)
    else:
        user = User.objects.get(username=request.POST['username'])
        print("password match")
        request.session['id'] = user.id
        request.session['username']=user.username
        print(request.session['id'])
        return redirect(dashboard)


def dashboard(request):
    plans= Plan.objects.filter(added_by_id=request.session['id'])
    joins=Join.objects.filter(added_user_id=request.session['id'])
    destinations=Plan.objects.exclude(added_by_id=request.session['id'])
    
    context={
        'joins': joins,
        'plans': plans,
        'destinations': destinations 
    }

    return render(request,'travels.html',context)

def add(request):
    return render(request,'add.html')

def create(request):
    errors = Plan.objects.plan_validator(request.POST)
    print(errors)
    if len(errors)>0:
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)


        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect(add)

    else:
        Plan.objects.create(description=request.POST['description'], destination=request.POST['destination'], 
        start= request.POST['travel_from'], end=request.POST['travel_to'],added_by_id=request.session['id'])
        return redirect(dashboard)

def destination(request,plan_id):
    user=Plan.objects.get(id=plan_id)
    join=Join.objects.filter(added_plan_id=plan_id)
    context={'users':user,
            'joins': join
    }
    return render(request,'destination.html',context)

def join(request,destination_id):
    Join.objects.create(added_plan_id=destination_id, added_user_id=request.session['id'])
    
    return redirect(dashboard)

def logout(request):
    request.session.clear()
    return redirect(index)