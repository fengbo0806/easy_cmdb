from django.db import models
from configureBaseData.models.venders import Vender, VenderStaff


# Create your models here.
class Machine(models.Model):
    '''
    the detail information for machine, just the basic info.
    '''
    machineLocate = models.ForeignKey('MachineLocate', on_delete=models.CASCADE, blank=True, null=True)
    machineVender = models.ForeignKey('Vender', on_delete=models.CASCADE, blank=True, null=True)
    machineAssetNumber = models.CharField(max_length=255)
    machineOs = models.CharField(max_length=255)
    machineType = models.ForeignKey('MachineType', on_delete=models.CASCADE, blank=True, null=True)
    machineEthNum = models.IntegerField()
    loginUser = models.CharField(max_length=255, blank=True, null=True)
    loginMethod = models.CharField(max_length=255, blank=True, null=True)
    loginPort = models.IntegerField()

    # machine_service = models.CharField()
    # machine_admin = models.CharField()
    def __str__(self):
        return str(self.machineAssetNumber)

    class Meta:
        verbose_name = '机器'


class MachineType(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name = '设备类型'


class MachineRoom(models.Model):
    '''
    describ the address of IDC, maybe some detail information for contant of the service stuff
    '''
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    note = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '机房'


class MachineRack(models.Model):
    '''
    describe the detail maching rack locate
    '''
    floor = models.IntegerField()
    locate = models.CharField(max_length=30)
    note = models.CharField(max_length=30)
    room = models.ForeignKey('MachineRoom', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.room) + ':' + str(self.floor) + '楼:' + str(self.locate) + '柜'

    class Meta:
        verbose_name = '机架'


class MachineLocate(models.Model):
    '''
    describe the macing locate
    '''
    Ulocate = models.IntegerField()
    rack = models.ForeignKey('MachineRack', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('Ulocate', 'rack')
        verbose_name = '设备位置'

    def __str__(self):
        return str(self.rack) + '-U' + str(self.Ulocate)
