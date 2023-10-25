from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('check-username/', views.checkUsernameAvailability,
         name='check-username-availability'),
    path('check-email/', views.checkEmailAvailability,
         name='check-email-availability'),
    path('check-phone/', views.checkPhoneAvailability,
         name='check-phone-availability'),
    path('send-email-otp/', views.sendEmailOtp, name='send-email-otp'),
    path('send-phone-otp/', views.sendPhoneOtp, name='send-phone-otp'),
    path('update-email/', views.updateEmail, name='update-email'),
    path('sent-email-update-otp/', views.sendEmailUpdateOtp,
         name='sent-email-update-otp'),
    path('verify-and-update-data/', views.verifyAndUpdate,
         name='verify-and-update-data'),
    path('update-profile/', views.updateProfile, name='update-profile'),
    path('get-profile/', views.getUserProfile, name='get-profile'),
]
