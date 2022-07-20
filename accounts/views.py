from django.shortcuts import render, redirect
from django.contrib import messages, auth

from django.contrib.auth.decorators import login_required

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

            messages.success(request, 'Registration successful, please check your inbox to activate the email')
            return redirect('register-user')
        
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
