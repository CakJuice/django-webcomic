from django.shortcuts import render, get_object_or_404

from .models import UserActivation


# Create your views here.
def user_activation(request, token):
    activation = get_object_or_404(UserActivation, token=token)
    user = activation.user
    user.is_active = True
    user.save()
    return render(request, 'user/user_activation_success.html')

