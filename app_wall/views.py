from django.shortcuts import redirect, render, HttpResponse
from.models import *
from django.contrib import messages


# Create your views here.
def index(request):
     return render(request,'log_in.html')


def log_reg(request):
     if request.method == 'POST':
          errors = User.objects.basic_validator(request.POST)
          if len(errors) > 0:
               for key, value in errors.items():
                    messages.error(request,value)
               return redirect("/")
          first_name = request.POST['first_name']
          last_name = request.POST['last_name']
          email = request.POST['email']
          password = request.POST['password']
          hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
          User.objects.create(first_name=first_name, last_name= last_name, email=email, password= hash_pw)
          return redirect ('/')

def log_in(request):
     if request.method == "POST":
          email = request.POST['email']
          password = request.POST['password']
          if not User.objects.authenticate(email, password):
               messages.error(request, 'Email and password do not match')
               return redirect("/")
          user = User.objects.get(email=email)
          request.session['user_id'] = user.id
          return redirect ("/logged")
     return redirect('/')

def logged(request):
     if 'user_id' not in request.session:
          return HttpResponse('<h1>You must be logged in</h1>')
     user = User.objects.get(id= request.session['user_id'])
     context = {
               "user": user
          }
     return render(request, 'logged.html',context)

def add_post(request):
     post_text = request.POST['post_text']
     errors = Post.objects.validate_post(post_text)
     if len(errors) > 0:
          for key, val in errors.items():
               messages.error(request, val)
          return redirect('/logged')
     user = User.objects.get(id= request.session['user_id'])
     Post.objects.create(text=post_text, user= user)
     return redirect('/wall_feed')

def wall_feed(request):
     all_posts = Post.objects.all()
     context = {
          'all_posts': all_posts
     }
     return render(request, 'feed.html', context)

def edit_post(request, id):
     post_to_edit = Post.objects.get(id = id)
     context = {
          "post": post_to_edit
     }
     return render(request, 'edit.html', context)

def edited_post(request):
     if request.method == "POST":
          post_id = request.POST['id']
          new_text = request.POST['post_text']
          errors = Post.objects.validate_post(new_text)
          if len(errors) > 0:
               for key, val in errors.items():
                    messages.error(request, val)
               return redirect('/logged')
          post_to_edit = Post.objects.get(id = post_id)
          post_to_edit.text = new_text
          post_to_edit.save()
          return redirect('/wall_feed')
          
def add_comment(request):
     comment_text = request.POST['comment_text']
     post_id = request.POST['post_id']
     user = User.objects.get(id = request.session['user_id'])
     post = Post.objects.get(id = post_id)
     Comment.objects.create(text= comment_text, user= user, post=post)
     return redirect('/wall_feed')

def logout(request):
     del request.session['user_id']
     return redirect('/')
     
     
          

# def add_comment_wallmsg(request, id):
#      # create comment to the wall message
#      user_poster = User.object.get(id=)