from django.contrib import admin
from .models import author_data, otp_generator

# Register your models here.
admin.site.register(author_data)
admin.site.register(otp_generator)