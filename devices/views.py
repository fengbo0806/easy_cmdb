from django.shortcuts import render
# from django.http import HttpResponse
from configureBaseData.models.devices import *
from configureBaseData.models.ips import *
from configureBaseData.models.venders import *
from configureBaseData.models.processes import *


# import datetime
def listAllDev(request):
    # listDevice = Machine.objects.filter(id=1)
    # listDevice = Machine.objects.get(pk=1)
    # lisIP = IpV4.objects.filter(MachineIp=listDevice).all()
    listAdminIP = IpV4.objects.filter(isManage=True).select_related('MachineIp').all()
    print(listAdminIP.query)
    for items in listAdminIP:
        print(items.MachineIp.machine_asset_number)

    return render(request, 'devices/listall.html', {'listDevice': listAdminIP})


def rebootDev(request):
    import devices.deviceOperater as operater
    listDevice = 'reboot'
    return render(request, 'devices/devices.html', {'listdevice': listDevice})


def detailDev(request):
    if request.method=='GET':
        nid = int(request.GET.get('nid'))
        deviceInfo = Machine.objects.get(id=nid)
        deviceIp = IpV4.objects.filter(MachineIp=deviceInfo)
        deviceProcess = process.objects.filter(runMachine=deviceInfo)
    elif request.method=='POST':
        pass

    # print(deviceProcess.query)
    return render(request, 'devices/detail.html', {'deviceInfo': deviceInfo, 'deviceIp': deviceIp,'deviceProcess':deviceProcess})
