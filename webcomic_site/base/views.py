from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignupForm


# Create your views here.
def homepage(request):
    """ Display homepage request.
    :param request: Page request.
    :return: Renderer page for user with template as param.
    """
    return render(request, 'base/homepage.html')


def signup(request):
    """ Handle signup/registration for new user.
    :param request: Page request.
    :return: Renderer page for user with template and context as params.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('signup_success', username=user.username)
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'base/signup.html', context)


def signup_success(request, username):
    """ Handle user signup success.
    :param request: Page request.
    :param username: Username of signup user.
    :return: If there is valid username in param, it will render signup_success page, otherwise it will be
    redirect to 404.
    """
    user = get_object_or_404(User, username=username)
    return render(request, 'base/signup_success.html', context={'email': user.email})
