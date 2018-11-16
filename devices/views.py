from django.shortcuts import render
# from django.http import HttpResponse
from configureBaseData.models.devices import *
# import datetime
def listAllDev(request):
    listDevice = Machine.objects.all()
    return render(request,'devices/devices.html',{'listdevice':listDevice})
def rebootDev(request):
    import devices.deviceOperater as operater

    listDevice = 'reboot'
    return render(request,'devices/devices.html',{'listdevice':listDevice})