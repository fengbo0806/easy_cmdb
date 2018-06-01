from django.contrib import admin
from .models import *
# Register your models here.
class IpV4_admin(admin.ModelAdmin):
    pass
admin.site.register(IpV4,IpV4_admin)
