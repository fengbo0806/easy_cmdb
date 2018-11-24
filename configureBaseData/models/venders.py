from django.db import models
from .businesses import *


# Create your models here.
class Vender(models.Model):
    '''
    vender
    '''
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    business = models.ForeignKey('Business', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)


class VenderStaff(models.Model):
    '''
    the works of vender
    '''
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=128, blank=True)
    company = models.ForeignKey('Vender', on_delete=models.CASCADE)
    phone = models.IntegerField()
    wechat = models.CharField(max_length=60, blank=True)
    mail = models.CharField(max_length=60, blank=True)
    qq = models.IntegerField(blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)
