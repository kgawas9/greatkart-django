from email.message import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from .models import Account

from .forms import RegistrationForm

# Create your views here.

def register_user(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            username = email.split("@")[0]

            user = Account.objects.create_user(first_name = first_name,
                            last_name = last_name,
                            email = email,
                            username = username,
                            password = password)

            user.phone_number = phone_number
            user.save()

            # to send an email
            # ================================
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Thank you for registering with us! we have sent a verification link to your email address, please check your inbox to verify the account')
            return redirect('/accounts/login/?command=verification&email='+email)
            # ================================
        
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context=context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials!')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    name = request.user.first_name
    auth.logout(request)
    messages.info(request, 'See you soon, ' + str(name))
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! your account has activated successfully')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        is_account_exist = Account.objects.filter(email=email).exists()

        if not is_account_exist:
            messages.error(request, 'Account with this id is not exist, please check your email address')
            return redirect('forgot-password')
        
        user = Account.objects.get(email__iexact=email)
        # to send an email
            # ================================
        current_site = get_current_site(request)
        mail_subject = 'Reset your password'
        message = render_to_string('accounts/reset-password-email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        messages.success(request, 'Password reset email has been successfully sent to your email address.')
        return redirect('login')
    return render(request, 'accounts/forgot-password.html')


def reset_password_validate(request):
    return
