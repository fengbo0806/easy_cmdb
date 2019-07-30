from django.db import models
from .businesses import *


# Create your models here.
class VideoSupplier(models.Model):
    '''
    ProgramSupplier
    '''
    chinaname = models.CharField(max_length=255)
    englishname = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    def __str__(self):
        return str(self.chinaname)

    class Meta:
        verbose_name = '信源供应商'
        verbose_name_plural = '信源供应商'


class SupplyProgram(models.Model):
    '''
    ProgramSupplier
    '''
    programname = models.CharField(max_length=255)
    programtype = models.CharField(max_length=255,null=True, blank=True, default=None)
    aliasname = models.CharField(max_length=255, null=True, blank=True, default=None)
    note = models.TextField(null=True, blank=True, default=None)
    vender = models.ForeignKey('VideoSupplier', on_delete=models.CASCADE)
    height = models.IntegerField(default=0, blank=True)
    width = models.IntegerField(default=0, blank=True)
    bandwidth = models.IntegerField(default=0, blank=True)
    inPutType = models.CharField(max_length=255, null=True, blank=True)
    inPutStream = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.programname)

    class Meta:
        verbose_name = '上游频道'
        verbose_name_plural = '上游频道'


class SupplierStaff(models.Model):
    '''
    the works of vender
    '''
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=128, blank=True)
    company = models.ForeignKey('VideoSupplier', on_delete=models.CASCADE)
    phone = models.IntegerField()
    wechat = models.CharField(max_length=60, blank=True)
    mail = models.CharField(max_length=60, blank=True)
    qq = models.IntegerField(blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '信源供应商人员'
        verbose_name_plural = '信源供应商人员'
