from configureBaseData.models.encoderserver import *
from configureBaseData.models.ips import *
from configureBaseData.models.devices import *

'''

'''


def getTargetIp():
    '''
           {'0': [{'id': '0', 'status': '-1', 'name': '银川公共-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}],
           '1': [{'id': '1', 'status': '-1', 'name': '杭州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}],
           '2': [{'id': '2', 'status': '0', 'name': '广州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}],
           '3': [{'id': '3', 'status': '0', 'name': '福州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}],
           '4': [{'id': '4', 'status': '0', 'name': '郑州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}],
           '5': [{'id': '5', 'status': '0', 'name': '兰州新闻-公网天维', 'width': '720', 'height': '576', 'outbandwidth': '2500'}]}
    '''
    query = Machine.objects.filter(ipv4__isManage='True', machine_type=1).values('ipv4__ip', )
    for i in query:
        print(i)
