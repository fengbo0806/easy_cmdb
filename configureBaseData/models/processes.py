from django.db import models
from configureBaseData.models.devices import Machine
from configureBaseData.models.businesses import Business


class process(models.Model):
    aliasName = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=255, )
    runMachine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True, blank=True)
    typeOfProcess = models.ForeignKey(typeOfProcess, on_delete=models.SET_NULL, null=True, blank=True)
    '''
    may add the operate of yaml, install pyyaml
    '''

class services(models.Model):
    alisName = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=255)
    runMachine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True, blank=True)
    typeOfProcess = models.ForeignKey(typeOfProcess, on_delete=models.SET_NULL, null=True, blank=True)


class typeOfProcess(models.Model):
    name = models.CharField(max_length=255)
    typeOfBusinesses = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True)

