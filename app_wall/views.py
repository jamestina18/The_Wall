from django.shortcuts import redirect, render, HttpResponse
from.models import *
from django.contrib import messages

# Create your views here.
def index(request):
     return HttpResponse(" This is just a test ")

def logged(request):
     if 'user' not in request.session:
          return redirect('/')
     context = {
               'walll_messages':Wall_Msg.objects.all()
          }
     return render(request, 'loggen.html',context)

def add_user(request):
     errors - User.objects.basic_validator(request.POST)
     if len(errors)>0:
          for key, value in errors.items():
               messages.error(request,value)
          return redirect('/')
     new_user = User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=request.POST['pw'])


def post_wall_msg(request):
     pass

def add_comment_wallmsg(request, id):
     # create comment to the wall message
     user_poster = User.object.get(id=)