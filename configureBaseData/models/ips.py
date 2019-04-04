from django.db import models
from .devices import Machine


# Create your models here.
class IpV4(models.Model):
    vlan = models.IntegerField(default=0)
    ip = models.GenericIPAddressField()
    MachineIp = models.ForeignKey(Machine, on_delete=models.CASCADE, blank=True, null=True)
    isHttpManage = models.BooleanField(default=False)
    isSshManage = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ip)

    class Meta:
        verbose_name = 'IP地址'
        verbose_name_plural = 'IP地址'
