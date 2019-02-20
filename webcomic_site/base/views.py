from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import UserActivation
from .forms import SignupForm

from webcomic_site.comic.models import Comic


# Create your views here.
def homepage(request):
    """ Display homepage request.
    :param request: Page request.
    :return: Renderer page for user with template as param.
    """
    comics = Comic.objects.all()
    context = {
        'comics': comics
    }
    return render(request, 'base/homepage.html', context=context)


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
            activation = UserActivation.objects.create(user=user)
            activation.send_mail_activation(request)
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


def user_activation(request, token):
    """ Handle user account activation.
    :param request: Page request.
    :param token: Token of activation. If token invalid, page will render activation expire
    :return: If token valid, it will render success message. Otherwise, page will render activation expire.
    """
    activation = get_object_or_404(UserActivation, token=token, is_activated=False)
    if activation.activated():
        return render(request, 'base/user_activation_success.html')

    return render(request, 'base/user_activation_expire.html')
