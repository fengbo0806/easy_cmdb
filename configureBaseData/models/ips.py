from django.db import models

# Create your models here.
class IpV4(models.Model):
    vlan = models.IntegerField(default=0)
    ip = models.GenericIPAddressField()

