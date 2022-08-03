from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

#from orders.views import user_orders

from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from .tokens import account_activation_token


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request,
                  'account/user/dashboard.html',
                  {'section': 'profile', 'orders': orders})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):

    if request.user.is_authenticated:    # This will check if the user is already logged in. If he has then he need not register. So simply redirect him.
        return redirect('account:dashboard')

    if request.method == 'POST':  # We don't want to any one to register unless they have posted the data. So we check if there is a POST.
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():    # This will check if the details are valid and then saves the following fields/details
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']    # This clean is done for security purposes. Checks if the email is valid email and not somehing else
            user.set_password(registerForm.cleaned_data['password'])   # same as above.  insures no data is injecte
            user.is_active = False   # This field is present in models. we set it to false coz we want to do email verification
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'    # This is the message user will see in the mail.Ex"click the below link to activate your account"
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })   # The token parameter will generate the token.The above 4 parameters will be passed on to the "account_activation_email.html" template
            user.email_user(subject=subject, message=message)  # 'email_user' will be sending the email. We can use additional arguements
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:  # Here we are collecting the data that has been passed through
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):   # Checking if the user exists 
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html') 
