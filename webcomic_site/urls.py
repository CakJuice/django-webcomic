"""webcomic_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from webcomic_site.base import views as base_views
from webcomic_site.comic import views as comic_views

urlpatterns = [
    # base routes
    path('', base_views.homepage, name='homepage'),
    path('signup/', base_views.signup, name='signup'),
    path('<username>/signup-success/', base_views.signup_success, name='signup_success'),
    path('activation/<token>/', base_views.user_activation, name='user_activation'),
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='base/password_reset.html',
        email_template_name='base/password_reset_email.html',
        subject_template_name='base/password_reset_subject.txt'
    ), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='base/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='base/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='base/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name='base/password_change.html'
    ), name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='base/password_change_done.html'
    ), name='password_change_done'),

    # admin routes
    path('admin/', admin.site.urls),

    # ajax routes
    path('ajax/', include('webcomic_site.ajax.urls')),

    # genre routes
    path('genre/<slug:slug>/', comic_views.GenreDetailView.as_view(), name='genre_detail'),

    # comic routes
    path('comic/create/', comic_views.ComicCreateView.as_view(), name='comic_create'),
    # path('<slug:slug>/', comic_views.ComicDetailView.as_view(), name='comic_detail'),
    path('<slug:slug>/', comic_views.comic_detail, name='comic_detail'),
    path('<slug:slug>/update/', comic_views.ComicUpdateView.as_view(), name='comic_update'),
    path('<slug:slug>/update-state/<int:state>/', comic_views.action_state, name='comic_state'),

    # chapter routes
    path('<slug:comic_slug>/chapter/create/', comic_views.ChapterCreateView.as_view(), name='chapter_create'),
    path('<slug:comic_slug>/<slug:chapter_slug>/detail/', comic_views.ChapterDetailView.as_view(), name='chapter_detail'),
    path('<slug:comic_slug>/<slug:chapter_slug>/update/', comic_views.ChapterUpdateView.as_view(), name='chapter_update'),
    path('<slug:comic_slug>/<slug:chapter_slug>/add-image/', comic_views.ChapterImageCreateView.as_view(),
         name='chapter_add_image'),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
