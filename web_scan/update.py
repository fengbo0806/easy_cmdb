from configureBaseData.models.encoderserver import *
from configureBaseData.models.ips import *
from django.core.exceptions import ObjectDoesNotExist


# from django.db.models.expressions


def updateEncoderInfo():
    '''
    ip
    encoder
    device
    :return:
    '''
    messages = {'0': {'rowid': 0, 'switchStatus': True, 'name': '银川公共-公网天维', 'width': 576, 'height': 720,
                      'outbandwidth': '2500'},
                '1': {'rowid': 1, 'switchStatus': -True, 'name': '杭州新闻-公网天维', 'width': 720, 'height': 576,
                      'outbandwidth': '2500'},
                '2': {'rowid': 2, 'switchStatus': True, 'name': '广州新闻-公网天维', 'width': 576, 'height': 720,
                      'outbandwidth': '2500'},
                '3': {'rowid': 3, 'switchStatus': True, 'name': '福州新闻-公网天维', 'width': 576, 'height': 576,
                      'outbandwidth': '2500'},
                '4': {'rowid': 4, 'switchStatus': True, 'name': '郑州新闻-公网天维', 'width': 720, 'height': 576,
                      'outbandwidth': '2500'},
                '5': {'rowid': 5, 'switchStatus': True, 'name': '兰州新闻-公网天维', 'width': 720, 'height': 576,
                      'outbandwidth': '2500'}}
    tagMachine = Machine.objects.get(machineType__name='编码器')
    n=0
    for key in messages.keys():
        # print(messages[key])
        # ProgramDetail.objects.filter(machine_id=1).create(**messages[key])
        # print(messages[key]['rowid'])
        ProgramDetail.objects.update_or_create(machine_id=tagMachine.id,**messages[key])
        # try:
        #     ProgramDetail.objects.get(machine=tagMachine, rowid=messages[key]['rowid'])
        # except ProgramDetail.DoesNotExist:
        #     ProgramDetail.objects.create(machine=tagMachine, **messages[key])
        # else:
        #     # print(ProgramDetail.objects.get(machine=tagMachine, rowid=messages[key]['rowid']))
        #     ProgramDetail.objects.get(machine=tagMachine, rowid=messages[key]['rowid']).(**messages[key])
        # ProgramDetail.objects.get_or_create(machine=tagMachine, rowid=messages[key]['rowid'])

        # ProgramDetail.objects.save()
    print(n)

