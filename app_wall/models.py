from enum import auto
from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
# this is the class validator
class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        if len(postdata['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        if not EMAIL_REGEX.match(postdata['email']):
            errors['email'] = 'Email in not valid !'
        emailCheck = self.filter(email=postdata['email'])
        if emailCheck:
               errors['email'] = "Email is already in use"
        if len(postdata['first_name']) < 2 or len(postdata['last_name']) < 2:
            errors['name'] = "Your name must be at least 2 characters"
        
        if postdata['password'] != postdata['confirm_password']:
            errors['passsword'] = 'Password and Confirm Password do not match'
        return errors

    def authenticate(self,email, password):
        users = self.filter(email = email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())



class User(models.Model):
     first_name = models.CharField(max_length=50)
     last_name = models.CharField(max_length=50)
     email = models.EmailField(max_length=50)
     password = models.CharField(max_length=50)
     created_at = models.DateTimeField(auto_now_add=True, null=True)
     updated_at = models.DateTimeField(auto_now=True, null=True)

     # this is the validation obj it will validate the user input field
     objects = UserManager()
     def __str__(self):
        return f"{self.first_name} {self.last_name}{self.email} {self.id}"

# validation for the post so erreo message would show according to req
class PostManager(models.Manager):
    def validate_post(self, post_text):
        errors = {}
        if len(post_text) < 3:
            errors['length'] = 'Post must be at least 3 characters!'
        if len(post_text) > 299:
            errors['length'] = f'Post must not be more than 299 characters. This Post is {len(post_text)}'
        return errors



# this is for the initial post the user post on the wall
class Post(models.Model):
    text = models.CharField(max_length=299)
    user = models.ForeignKey(User, related_name= "posts", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = PostManager()

class Comment(models.Model):
    text = models.CharField(max_length=280)
    user = models.ForeignKey(User, related_name= "comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name= "comments", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null= True)
    updated_at = models.DateField(auto_now=True, null=True)

