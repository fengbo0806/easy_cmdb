from django.db import models
from configureBaseData.models.venders import Vender, VenderStaff


# Create your models here.
class Machine(models.Model):
    '''
    the detail information for machine, just the basic info.
    '''
    machine_locate = models.ForeignKey('MachingLocate', on_delete=models.CASCADE, blank=True, null=True)
    machine_vender = models.ForeignKey('Vender', on_delete=models.CASCADE, blank=True, null=True)
    machine_asset_number = models.CharField(max_length=255)
    machine_os = models.CharField(max_length=255)
    machine_eth_num = models.IntegerField()
    # machine_service = models.CharField()
    # machine_admin = models.CharField()


class MachineRoom(models.Model):
    '''
    describ the address of IDC, maybe some detail information for contant of the service stuff
    '''
    address = models.CharField(max_length=255)
    note = models.CharField(max_length=255)


class MachingRack(models.Model):
    '''
    describe the detail maching rack locate
    '''
    floor = models.IntegerField()
    locate = models.CharField(max_length=30)
    note = models.CharField(max_length=30)
    room = models.ForeignKey('MachineRoom', on_delete=models.CASCADE)


class MachingLocate(models.Model):
    '''
    describe the macing locate
    '''
    Ulocate = models.IntegerField()
    rack = models.ForeignKey('MachingRack', on_delete=models.CASCADE)
