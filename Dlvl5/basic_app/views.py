from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm,UserFrom

from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("you are an asshole")

def register(request):

      registered = False

      if request.method == 'POST':
          user_form = UserFrom(data = request.POST)
          profile_from = UserProfileInfoForm(data = request.POST)

          if user_form.is_valid() and profile_from.is_valid():

              user = user_form.save()
              user.set_password(user.password)
              user.save()

              profile = profile_from.save(commit=False)
              profile.user = user

              if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

              profile.save()
              registered = True

          else:
              print(user_form.errors,profile_from.errors)
      else:
            user_form = UserFrom()
            profile_from = UserProfileInfoForm()
      return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_from,'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username,password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account Not Active')
        else:
            return HttpResponse('Invalid User')
    else:
        return render(request,'basic_app/login.html',{})
