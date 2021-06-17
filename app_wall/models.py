from django.db import models

# Create your models here.
# this is the class validator
class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postdata['pw']) < 8:
            errors['pw'] = "Your password must be at least 8 characters"
        if len(postdata['fname']) < 2 or len(postdata['lname']) < 2:
            errors['name'] = "Your name must be at least 2 characters"
        if not email_checker.match(postdata['email']):
            errors['email'] = 'Email must be valid'
        if postdata['pw'] != postdata['confpw']:
            errors['pw'] = 'Password and Confirm Password do not match'
        return errors



class User(models.Model):
     first_name = models.CharField(max_length=50)
     last_name = models.CharField(max_length=50)
     email = models.CharField(max_length=50)
     password = models.CharField(max_length=50)

     # this is the validation obj it will validate the user input field
     objects = UserManager()

class Wall_Msg(models.Model):
     message = models.CharField(max_length=255)
     user_poster = models.ForeignKey(User,related_name='user_messages', on_delete=models.CASCADE)


class Comment_to_Msg(models.Model):
     comment_to_Msg = models.CharField(max_length=255)
     user_poster = models.ForeignKey(User,related_name='user_comment', on_delete=models.CASCADE)
     wall_message = models.ForeignKey(Wall_Msg, related_name= 'comment_to_message', on_delete=models.CASCADE)

     # user_likes = models.ManyToManyField(User, related_name='liked_post')