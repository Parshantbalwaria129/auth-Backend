from django.contrib import admin
from .models import UserProfile, EmailOtpModel, phoneOtpModel
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(EmailOtpModel)
admin.site.register(phoneOtpModel)
