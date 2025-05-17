"""
URL configuration for Lost_Found_Pets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from app.views import (UserView, RegisterUser, CustomTokenObtainPairView, Add_Raport, User_info, RaportsWithOneImageView,
                       Raport_Details, RaportsFiltered, UserRaportsView, UserRaportDetailView, UpdateUserRaportView, Confirm2FACodeView, SendRaportEmailView, LinkRaportsView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new_user/',RegisterUser.as_view(),name='new_user'),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_get"),  # URL rest framework do loginu
    path("logout/", TokenRefreshView.as_view(), name="token_refresh"),
    path("new_raport/", Add_Raport.as_view(), name="add_raport"),
    path("user_info/", User_info.as_view(), name="user_info"),
    path("change_password/", User_info.as_view(), name="changePass"),
    path('raports/', RaportsWithOneImageView.as_view(), name='raports'),
    path('raport_details/<int:pk>/', Raport_Details.as_view(), name='raport-detail'),
    path('raports-filtered/', RaportsFiltered.as_view(), name='raports_filtered'),
    path('user_raports/', UserRaportsView.as_view(), name='user_raports'),
    path('user_raport/<int:pk>/', UserRaportDetailView.as_view(), name='user_raport_detail'),
    path('update_user_raport/<int:pk>/', UpdateUserRaportView.as_view(), name='update_user_raport'),
    path('confirm-code/', Confirm2FACodeView.as_view(), name='confirm_2fa_code'),
    path('raport_details/<int:pk>/send_email/', SendRaportEmailView.as_view(), name='send_mail'),
    path('link-raports/', LinkRaportsView.as_view(), name='link_raports')
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)