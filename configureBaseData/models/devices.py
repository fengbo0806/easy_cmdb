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
    login_user = models.CharField(max_length=255, blank=True, null=True)
    login_method = models.CharField(max_length=255, blank=True, null=True)
    login_port = models.IntegerField()

    # machine_service = models.CharField()
    # machine_admin = models.CharField()
    def __str__(self):
        return str(self.machine_asset_number)


class MachineRoom(models.Model):
    '''
    describ the address of IDC, maybe some detail information for contant of the service stuff
    '''
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    note = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class MachingRack(models.Model):
    '''
    describe the detail maching rack locate
    '''
    floor = models.IntegerField()
    locate = models.CharField(max_length=30)
    note = models.CharField(max_length=30)
    room = models.ForeignKey('MachineRoom', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.room) + ':' + str(self.floor) + '楼:' + str(self.locate) + '柜'


class MachingLocate(models.Model):
    '''
    describe the macing locate
    '''
    Ulocate = models.IntegerField()
    rack = models.ForeignKey('MachingRack', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('Ulocate', 'rack')

    def __str__(self):
        return str(self.rack) + '-U' + str(self.Ulocate)
