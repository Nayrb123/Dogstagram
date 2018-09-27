from django.db import models
import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Za-z]+$')
# Create your models here.

class UserManager(models.Manager):
    def validator(self,postData):
        errors = {}
        print(postData)
        if len(postData['user_name']) < 3:
            errors['user_name'] = "Username should be at least 3 characters."
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters."
        if not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "First name must contain letters only"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        if not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Last name must contain letters only"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email"

        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Comment(models.Model):
    Comment = models.TextField()
    comment_uploader = models.ForeignKey(User, related_name="uploaded_comment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)