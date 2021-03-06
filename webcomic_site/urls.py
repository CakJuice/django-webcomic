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
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from webcomic_site.base import views as base_views
from webcomic_site.comic import views as comic_views
from webcomic_site.author import views as author_views

urlpatterns = [
    # homepage routes
    path('', base_views.homepage, name='homepage'),

    # base routes
    path('signup/', base_views.signup, name='signup'),
    path('<username>/signup-success/', base_views.signup_success, name='signup_success'),
    path('activation/<token>/', base_views.user_activation, name='user_activation'),
    path('login/', base_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/', base_views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='base/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', base_views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='base/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('settings/password/', base_views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='base/password_change_done.html'
    ), name='password_change_done'),

    # admin routes
    path('admin/', admin.site.urls),

    # api routes
    path('api/', include('webcomic_site.rest.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),

    # ajax routes
    path('ajax/', include('webcomic_site.ajax.urls')),

    # genre routes
    # path('genre/<slug:slug>/', comic_views.GenreDetailView.as_view(), name='genre_detail'),
    path('genre/<slug:slug>/', comic_views.genre_detail, name='genre_detail'),

    # user author routes
    path('profile/<username>/', author_views.AuthorDetailView.as_view(), name='author_detail'),

    # comic routes
    path('comic/create/', comic_views.ComicCreateView.as_view(), name='comic_create'),
    path('<slug:slug>/', comic_views.ComicDetailView.as_view(), name='comic_detail'),
    path('<slug:slug>/author-page/', comic_views.ComicAuthorPageView.as_view(), name='comic_author'),
    path('<slug:slug>/update/', comic_views.ComicUpdateView.as_view(), name='comic_update'),
    path('<slug:slug>/update-state/<int:state>/', comic_views.action_state, name='comic_state'),

    # chapter routes
    path('<slug:comic_slug>/chapter/create/', comic_views.ChapterCreateView.as_view(), name='chapter_create'),
    path('<slug:comic_slug>/<slug:chapter_slug>/', comic_views.ChapterDetailView.as_view(),
         name='chapter_detail'),
    path('<slug:comic_slug>/<slug:chapter_slug>/author-page/', comic_views.ChapterAuthorPageView.as_view(),
         name='chapter_author'),
    path('<slug:comic_slug>/<slug:chapter_slug>/update/', comic_views.ChapterUpdateView.as_view(),
         name='chapter_update'),
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
