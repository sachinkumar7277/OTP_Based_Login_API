"""withoutREST URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from restAPI import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'login_otp_api/', views.Login_OTP.as_view()),

    path(r'logout/',views.logout_view, name='logout'),
    path(r'register/',views.register, name='register'),
    path(r'login/',views.login_OTP_request, name='login'),
    path('validate_otp/<str:phone>/',views.Validate, name='validate_otp'),
    path(r'',views.index)

    # path(r'search/', views.search),
    # path(r'load-states/',views.States, name='ajax_load_states'),
    # path(r'load-dists/',views.Districts, name='ajax_load_dists'),
    # path(r'api/', views.emp_data_view),
    # path(r'jsonapi/', views.emp_data_Json_view),
    # path(r'jsonRESPOapi/', views.emp_data_JsonRESPO_view),
    # path(r'apii/<int:id>/', views.JsonCBV.as_view()),
    # path(r'serialapi/<int:id>/', views.serializerapi.as_view()),
    # path(r'serialapi/', views.serializerapi.as_view()),  """
    # path(r'otpapi/', views.OTP.as_view()),
    # path(r'logout/',views.logout_view, name='logout'),
    # path(r'register/',views.register, name='register'),
    # path(r'login/',views.login_OTP_request, name='login'),
    # path('validate_otp/<str:phone>/',views.Validate, name='validate_otp'),
    # path(r'',views.index)



]

if settings.DEBUG:
    urlpatterns=urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns=urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)