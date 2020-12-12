from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage

from .utils import generate_token
from .forms import CreateUserForm 


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password=password)
        
        if user is not None:
            login(request, user)
            messages.info(request, "Logged in as " + str(user.username))
            return redirect('/')
        else:
            messages.info(request, 'Username or Password is Incorrect or Activate your account from if not activated yet.')

    return render(request, 'auth/login.html')


@login_required(login_url='myOauth:login')
def user_logout(request):
    logout(request)
    return redirect("myOauth:login")

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            current_site = get_current_site(request) #to get our current domain
            email_subject = 'Activate Your Account'
            # print("printing User primary Key", user.pk)

            message = render_to_string('auth/activate.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)
            })

            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data.get('email')]
            )

            email.send()

            messages.info(request, "Profile Created Successfully for: "+ username)
            messages.info(request, "An verification link is send to your email please verify it to Activate your acccount.")
            return redirect("/")
        else:
            print("Form not valid")
            messages.error(request, "Try Entering Good Quality Password, or Check that your passwords Match.")

    return render(request, 'auth/register.html')

def not_found(request):
    return render(request, 'auth/404.html')

def logoutPage(request):
    print(request.user)
    return render(request, 'auth/logoutPage.html')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
            
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account Activated Successfully.")
            return redirect('/')

        return redirect("auth:not_found")