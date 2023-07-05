from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

def user_login(request):
    if request.method == "POST":
      username = request.POST["username"]
      password = request.POST["password"]
      user = authenticate(request, username=username, password=password)
      if user is not None:
          login(request, user)
          # Redirect to a success page.
          messages.success(request, ('You logged in successfully.'))
          return redirect('home')
      else:
          # Return an 'invalid login' error message.
          messages.success(request, ('There was an error logging in. Please try again...'))
          return redirect('login')
    else:
      return render(request, 'login.html', {})

def user_logout(request):
    logout(request)
    messages.success(request, ('You were logged out successfully.'))
    return redirect('home')

def user_register(request):
    if request.method == "POST":
      form = UserRegistrationForm(request.POST)
      if form.is_valid():
          form.save()
          username = form.cleaned_data['username']
          password = form.cleaned_data['password1']

          # Sign them in when they sign up
          user = authenticate(username=username, password=password)
          login(request, user)
          messages.success(request, ('You signed up successfully.'))
          return redirect('home')
    else:
      form = CustomUserCreationForm()

    return render(request, 'user_register.html', {
         'form': form,
      })