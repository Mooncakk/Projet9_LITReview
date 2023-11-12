"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from LITReview import settings
from accounts.views import signup, log_user, logout_user
from website.views import (home, create_ticket, flux, posts, follow_page, search_user, follow, unfollow,  ticket_view,
                           update_ticket, delete_ticket, create_review_from_ticket, create_review_and_ticket,
                           update_review, review_view, delete_review)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('login/', log_user, name='connexion'),
    path('signup/', signup, name='inscription'),
    path('logout/', logout_user, name='déconnexion'),
    path('flux/', flux, name='flux'),
    path('posts/', posts, name='posts'),
    path('follow/', follow_page, name='page_abonnement'),
    path('searched-user/', search_user, name='utilisateur_recherché'),
    path('follow/<str:pk>/', follow, name="s'abonner"),
    path('unfollow/<str:pk>/', unfollow, name='désabonner'),



    path('create-ticket/', create_ticket, name='création_ticket'),
    path('update-ticket/<str:pk>/', update_ticket, name='modifier_ticket'),
    path('ticket/<str:pk>/', ticket_view, name='ticket'),
    path('delete-ticket/<str:pk>/', delete_ticket, name='supprimer_ticket'),

    path('create-review/ticket/<str:pk>/', create_review_from_ticket, name='création_critique_en_réponse'),
    path('create-review-and-ticket/', create_review_and_ticket, name='création_critique_et_ticket'),
    path('update-review/<str:pk>/', update_review, name='modifier_critique'),
    path('review/<str:pk>/', review_view, name='critique'),
    path('delete-review/<str:pk>', delete_review, name='supprimer_critique')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
