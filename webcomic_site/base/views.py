from django.shortcuts import render


# Create your views here.
def homepage(request):
    """ Display homepage request.
    :param request: User request.
    :return: Renderer page for user with template as param.
    """
    return render(request, 'base/homepage.html')
