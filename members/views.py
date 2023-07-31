from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from members.models import CustomUser
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token

def user_login(request):
    if request.method == "POST":
      username = request.POST["username"]
      password = request.POST["password"]
      user = authenticate(request, username=username, password=password)
      if user is not None:
          login(request, user)
          # Redirect to a success page.
          messages.success(request, ('You logged in successfully.'))
          u = CustomUser.objects.get(username = username)
          if u.verified is not True:
             messages.warning(
                request,
                mark_safe(
                f'You haven\'t verified your email. Do you want to \
                    <a href="members/send_confirmation">resend a confirmation email</a> \
                    to { u.email }?'
                )
             )
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
      form = CustomUserCreationForm(request.POST)
      if form.is_valid():
          form.save()
          username = form.cleaned_data['username']
          password = form.cleaned_data['password1']

          # Sign them in when they sign up
          user = authenticate(username=username, password=password)
          login(request, user)
          # messages.success(request, ('You signed up successfully.'))
          activateEmail(request)
          return redirect('home')
    else:
      form = CustomUserCreationForm()

    return render(request, 'user_register.html', {
         'form': form,
      })

def activateEmail(request):
    user = request.user
    mail_subject = 'Welcome to splitgal4.org'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
      messages.success(
        request, f'Dear {user}, please go to you email ({to_email}) \
          inbox and click on received activation link to confirm and complete \
          the registration. If you don\'t see it in a few minutes, please check \
          your spam folder.'
      )
    else:
        messages.error(request, f'Problem sending confirmation email to \
                       {to_email}, check if you typed it correctly.')
        
    return redirect('home')
        
def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        user.save()

        messages.success(request, 'Thank you for your confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('home')

def user_update(request, username):
    this_user = CustomUser.objects.get(username=username)
    form = CustomUserChangeForm(instance=this_user)

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=this_user)
        if form.is_valid():
            form.save()
            messages.success(request, ('Your account have been updated.'))
        else:
            messages.error(request, (form.errors['__all__']))
    else:
        form = CustomUserChangeForm(instance=this_user)
        
    return render(request, 'user_edit.html', {
         'form': form,
         'this_user': this_user
      })

def pw_update(request, username):
    this_user = CustomUser.objects.get(username=username)
    form = CustomPasswordChangeForm(user=this_user)
    return render(request, 'user_edit.html', {
         'form': form,
         'this_user': this_user
      })