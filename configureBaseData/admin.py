from django.contrib import admin
from .models.devices import *
from .models.ips import *



# Register your models here.

@admin.register(Machine)
class deviceAdmin(admin.ModelAdmin):
    pass


@admin.register(IpV4)
class IpV4Admin(admin.ModelAdmin):
    pass
