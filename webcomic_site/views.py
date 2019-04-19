from django.http import Http404
from django.http import JsonResponse


class AjaxableResponseMixin:
    """Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors)
        return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'success': True,
                'redirect': self.get_success_url(),
            }
            return JsonResponse(data)
        return response


class UserResponseMixin:
    def dispatch(self, request, *args, **kwargs):
        """Override function.
        Handle detail view page.
        Need to check is comic / chapter state = publish.
        If comic / chapter not publish, then check whether the user is logged in.
        If the user logged in then check whether the user is comic author or superuser.
        If the user is the author then call super function.
        Otherwise raise 404 page.
        :param request: Page request.
        :param args: Arguments.
        :param kwargs: Keyword arguments.
        :return: If allowed then call super function. Otherwise raise 404 page.
        """
        obj = self.get_object()
        if request.user.is_authenticated:
            is_allowed = request.user.is_superuser or request.user == obj.author
        else:
            is_allowed = obj.state == 1

        print(is_allowed, request.user.is_superuser, request.user)
        if is_allowed:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class OnlyAuthorOrSuperuserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_allowed = False
        if request.user.is_authenticated:
            is_allowed = request.user.is_superuser or request.user == obj.author
        if is_allowed:
            return super().dispatch(request, *args, **kwargs)
        raise Http404
