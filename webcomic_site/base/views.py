from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

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
            user = form.save()
            auth_login(request, user)
            return redirect('homepage')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'base/signup.html', context)
