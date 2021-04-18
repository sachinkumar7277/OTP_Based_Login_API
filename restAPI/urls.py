from django.urls import path
from .import  views

urlpatterns=[
     path('register/',views.register, name='register'),
     path('login/',views.login_OTP_request, name='login'),
     path('validate_otp/<str:phone_number>/',views.Validate, name='validate_otp'),
     path('logout/',views.logout_view, name='logout'),
     path('',views.index, name='index')
]