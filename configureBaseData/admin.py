from django.contrib import admin
from .models.devices import *
from .models.ips import *
from .models.venders import *
from .models.processes import *
from .models.businesses import Business,Projects

# Register your models here.
'''
bussiness and project
'''


@admin.register(Business)
class BussinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'introduction')


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'introduction')


'''
ip address
'''


@admin.register(IpV4)
class IpV4Admin(admin.ModelAdmin):
    pass


class IpV4Line(admin.StackedInline):
    extra = 0
    fieldsets = ((None, {'fields': (('vlan', 'ip', 'isManage'),)},),)
    model = IpV4


'''
process
'''


class processLine(admin.StackedInline):
    extra = 0
    fieldsets = ((None, {'fields': (('aliasName', 'name', 'typeOfProcess'),)},),)
    raw_id_fields = ('runMachine',)
    model = process


class servicesLine(admin.StackedInline):
    extra = 0
    fieldsets = ((None, {'fields': (('aliasName', 'name', 'typeOfProcess'),)},),)
    raw_id_fields = ('runMachine',)
    model = services


@admin.register(typeOfProcesses)
class typeOfProcessAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('name', 'typeOfBusinesses'),), }),)
    list_display = ('name', 'typeOfBusinesses')


@admin.register(services)
class servicesAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('aliasName', 'name', 'typeOfProcess'),('runMachine'),), }),)
    list_display = ('aliasName', 'name', 'typeOfProcess')


'''
device
'''


@admin.register(Machine)
class deviceAdmin(admin.ModelAdmin):
    list_display = ('machine_locate', 'machine_vender', 'machine_asset_number', 'machine_os')
    inlines = [IpV4Line, processLine, ]


'''
Machinglocate
'''


class MachingLocateLine(admin.StackedInline):
    extra = 0
    fieldsets = ((None, {'fields': (('Ulocate',),)},),)
    model = MachingLocate


class MachingRackLine(admin.StackedInline):  # TabularInline
    extra = 0
    fieldsets = ((None, {'fields': (('floor', 'locate', 'note'),)},),)
    model = MachingRack


@admin.register(MachineRoom)
class machineRoomAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('name', 'address', 'note'),), }),)
    inlines = [MachingRackLine, ]
    list_display = ('name', 'address', 'note')


@admin.register(MachingRack)
class machineRackAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('floor', 'locate', 'note'),), }),)
    inlines = [MachingLocateLine, ]
    list_display = ('room', 'floor', 'locate', 'note')


'''vender'''


class VenderStaffLine(admin.StackedInline):  # TabularInline
    extra = 0
    fieldsets = ((None, {'fields': (('name', 'title',), ('phone', 'wechat', 'mail', 'qq', 'note'))},),)
    model = VenderStaff


@admin.register(Vender)
class machineRoomAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('name', 'note'),), }),)
    inlines = [VenderStaffLine, ]
    list_display = ('name', 'note')
