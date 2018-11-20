from django.db import models
from .devices import Machine


# Create your models here.
class IpV4(models.Model):
    vlan = models.IntegerField(default=0)
    ip = models.GenericIPAddressField()
    MachineIp = models.ForeignKey(Machine, on_delete=models.CASCADE, blank=True, null=True)
    isManage = models.BooleanField(default=False)
