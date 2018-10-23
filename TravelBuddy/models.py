from __future__ import unicode_literals
from django.db import models
from datetime import datetime

now = str(datetime.now())

class UserManager(models.Manager):
    def basic_validator(self, postData):

        print("POSTDATA is", postData)

        errors = {}
        #Name Validation
        if len(postData["name"]) < 3:
            errors["name"] = "Name is required!"
        
        elif User.objects.filter(name = postData["name"]):
            errors["name"] = "Name already exist in database!"

        #Username Validation
        if len(postData["username"]) < 3:
            errors["username"] = "Username is required!"

        elif User.objects.filter(username = postData["username"]):
            errors["username"] = "Username already taken,please choose a new one!"

        #Password Validation
        if len(postData['password']) < 8:
            errors['password'] = "please provide a valid password!"
        if postData['confirm_password'] != postData['password']:
            errors['password'] = "Hey, these passwords don't match!!"
        return errors

    def login_validator(self, postData):

        print("POSTDATA is", postData)

        errors = {}
        #Username Validation
        if len(postData["username"]) < 3:
            errors["username"] = "Username is required!"

        elif not User.objects.filter(username = postData["username"]):
            errors["username"] = "Username not found, please register!"

        #Password Validation
        if len(postData['password']) < 8:
            errors['password'] = "please provide a valid password!"
        
        elif not User.objects.filter(password=postData['password']):
            errors['password']='Wrong password, please try again'
        return errors

class PlanManager(models.Manager):

    def plan_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destination']='please provide a destination'
    
        if len(postData['description'])<1: 
            errors['description']='please provide a description'
        
        if len(postData['travel_from'])<1: 
            errors['description']='please provide a travel date from'
        elif postData['travel_from'] < now:
            errors["travel_from"] = "Please provide a future date!"
        
        if len(postData['travel_to'])<1: 
            errors['description']='please provide a travel date to'
        elif postData['travel_to'] < now:
            errors["travel_to"] = "Please provide a future date!"
        elif not postData['travel_from'] <postData['travel_to']:
            errors['The travel date from must be before the travel date to']
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __repr__(self):
        return f"User: {self.id} {self.username}"

class Plan(models.Model):
    description=models.CharField(max_length=255)
    destination=models.CharField(max_length=255)
    start=models.DateField(max_length=255)
    end=models.DateField(max_length=255)
    added_by=models.ForeignKey(User,related_name='users_plans',on_delete=models.CASCADE)
    
    objects=PlanManager()



class Join(models.Model):
    added_user=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    added_plan=models.ForeignKey(Plan,related_name='plan',on_delete=models.CASCADE)




