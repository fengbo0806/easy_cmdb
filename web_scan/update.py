from threading import Thread
from multiprocessing import Process
import django
import sys
import os
import time
'''
the django enviormant just for test ,while the code on line ,delete it
'''
# 将项目路径添加到系统搜寻路径当中，查找方式为从当前脚本开始，找到要调用的django项目的路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 设置项目的配置文件 不做修改的话就是 settings 文件
os.environ['DJANGO_SETTINGS_MODULE'] = 'easy_cmdb.settings'
django.setup()
# from django.db.models.expressions
from configureBaseData.models.encoderserver import *
from configureBaseData.models.ips import *
from django.core.exceptions import ObjectDoesNotExist
class updateEncoder():
    '''
    input a list like [{ip:ip,type:type,}], use web_auth.py get encoder data,update database
    ip
    encoder
    device
    :return:
    '''

    def __init__(self):
        pass

    def updateInfo(self):
        '''
        updata whole encoder data
        :return:
        '''
        messages = {0: {'id': '0', 'switchstatus': True, 'name': '移动直播01', 'programstatus': -1, 'outbandwidth': '2000',
                        'width': '960', 'height': '540', 'inPutFirst': 'rtmp://play.news.ghwx.com.cn/live1/ch ',
                        'outPutFirst': 'udp://@228.1.2.140:1000', 'outPutSecond': 'http://10.78.64.195:1235/live01',
                        'outPutHttpFlow': 'http://10.78.64.195:1235/live01'},
                    1: {'id': '1', 'switchstatus': True, 'name': '移动直播02', 'programstatus': -1, 'outbandwidth': '2000',
                        'width': '1280', 'height': '720', 'inPutFirst': 'rtmp://juyunlive.juyun.tv/live/17147132 ',
                        'outPutFirst': 'udp://@228.1.2.140:2000', 'outPutSecond': 'http://10.78.64.195:1236/live02',
                        'outPutHttpFlow': 'http://10.78.64.195:1236/live02'},
                    2: {'id': '2', 'switchstatus': True, 'name': '移动直播03', 'programstatus': -1, 'outbandwidth': '2000',
                        'width': '1280', 'height': '720', 'inPutFirst': 'rtmp://play.news.ghwx.com.cn/live2/channel2 ',
                        'outPutFirst': 'udp://@228.1.2.140:3000', 'outPutSecond': 'http://10.78.64.195:1237/live03',
                        'outPutHttpFlow': 'http://10.78.64.195:1237/live03'},
                    3: {'id': '3', 'switchstatus': True, 'name': '移动直播04', 'programstatus': -1, 'outbandwidth': '2000',
                        'width': '1280', 'height': '720',
                        'inPutFirst': 'rtmp://rtmpdist-w.quklive.com/live/w1553663022875771 ',
                        'outPutFirst': 'udp://@228.1.2.140:4000', 'outPutSecond': 'http://10.78.64.195:1238/live04',
                        'outPutHttpFlow': 'http://10.78.64.195:1238/live04'},
                    4: {'id': '4', 'switchstatus': True, 'name': '移动直播05', 'programstatus': -1, 'outbandwidth': '2000',
                        'width': '1280', 'height': '720', 'inPutFirst': 'http://192.168.169.12:8088/lianghui1 ',
                        'outPutFirst': 'http://10.78.64.195:1239/live05',
                        'outPutHttpFlow': 'http://10.78.64.195:1239/live05', 'outPutSecond': 'udp://@228.1.2.140:5000'},
                    5: {'id': '5', 'switchstatus': True, 'name': '移动直播06', 'programstatus': -1, 'outbandwidth': '2000',
                        'width': '1280', 'height': '720', 'inPutFirst': 'http://192.168.169.12:8088/lianghui1 ',
                        'outPutFirst': 'http://10.78.64.195:1240/live06',
                        'outPutHttpFlow': 'http://10.78.64.195:1240/live06', 'outPutSecond': 'udp://@228.1.2.141:1000'},
                    6: {'id': '6', 'switchstatus': True, 'name': '移动直播07', 'programstatus': '3161[Q:30%]',
                        'outbandwidth': '2000', 'width': '1280', 'height': '720',
                        'inPutFirst': 'rtmp://3357.liveplay.myqcloud.com/live/3357_43011163691611e6a2cba4dcbef5e35a ',
                        'outPutFirst': 'http://10.78.64.195:1241/live07',
                        'outPutHttpFlow': 'http://10.78.64.195:1241/live07', 'outPutSecond': 'udp://@228.1.2.141:2000'},
                    7: {'id': '7', 'switchstatus': True, 'name': '移动直播08', 'programstatus': -1, 'outbandwidth': '2000',
                        'width': '1280', 'height': '720',
                        'inPutFirst': 'http://dl.live.cntv.cn/direct_play?rid=10061&role=Creator ',
                        'outPutFirst': 'http://10.78.64.195:1242/live08',
                        'outPutHttpFlow': 'http://10.78.64.195:1242/live08', 'outPutSecond': 'udp://@228.1.2.141:3000'},
                    8: {'id': '8', 'switchstatus': True, 'name': '移动直播09', 'programstatus': -1, 'outbandwidth': '2000',
                        'width': '1280', 'height': '720',
                        'inPutFirst': 'rtmp://59.110.126.141/live/CCTV158b49aab907944541a2587b5e2a534adfH ',
                        'outPutFirst': 'http://10.78.64.195:1243/live09',
                        'outPutHttpFlow': 'http://10.78.64.195:1243/live09', 'outPutSecond': 'udp://@228.1.2.141:4000'},
                    9: {'id': '9', 'switchstatus': True, 'name': '移动直播10', 'programstatus': -1, 'outbandwidth': '4000',
                        'width': '960', 'height': '540', 'inPutFirst': 'rtmp://10.78.43.20/wxmlive/skating ',
                        'outPutFirst': 'http://10.78.64.195:1244/live10',
                        'outPutHttpFlow': 'http://10.78.64.195:1244/live10', 'outPutSecond': 'udp://@228.1.2.141:5000'},
                    10: {'id': '10', 'switchstatus': True, 'name': '移动直播11', 'programstatus': -1,
                         'outbandwidth': '4000', 'width': '960', 'height': '540', 'inPutFirst': '0 ',
                         'outPutFirst': 'udp://@228.1.2.144:1000', 'outPutSecond': 'http://10.78.64.195:1245/live11',
                         'outPutHttpFlow': 'http://10.78.64.195:1245/live11'},
                    11: {'id': '11', 'switchstatus': True, 'name': '移动直播12', 'programstatus': -1,
                         'outbandwidth': '4000', 'width': '960', 'height': '540',
                         'inPutFirst': 'http://192.168.169.12:8088/lianghui2 ',
                         'outPutFirst': 'udp://@228.1.2.144:2000', 'outPutSecond': 'http://10.78.64.195:1246/live12',
                         'outPutHttpFlow': 'http://10.78.64.195:1246/live12'},
                    12: {'id': '12', 'switchstatus': True, 'name': '移动直播13', 'programstatus': -1,
                         'outbandwidth': '1000', 'width': '960', 'height': '540',
                         'inPutFirst': 'rtmp://rtmpdist-w.quklive.com/live/w1537255242556775 ',
                         'outPutFirst': 'udp://@228.1.2.144:3000', 'outPutSecond': 'http://10.78.64.195:1247/live13',
                         'outPutHttpFlow': 'http://10.78.64.195:1247/live13'},
                    13: {'id': '13', 'switchstatus': True, 'name': '移动直播14', 'programstatus': -1,
                         'outbandwidth': '1000', 'width': '960', 'height': '540',
                         'inPutFirst': 'http://dl.live.cntv.cn/direct_play?rid=10061&role=Creator ',
                         'outPutFirst': 'udp://@228.1.2.144:4000', 'outPutSecond': 'http://10.78.64.195:1248/live14',
                         'outPutHttpFlow': 'http://10.78.64.195:1248/live14'},
                    14: {'id': '14', 'switchstatus': True, 'name': '移动直播15', 'programstatus': -1,
                         'outbandwidth': '1000', 'width': '960', 'height': '540',
                         'inPutFirst': 'rtmp://rtmpdist-w.quklive.com/live/w1542682109696713 ',
                         'outPutFirst': 'udp://@228.1.2.144:5000', 'outPutSecond': 'http://10.78.64.195:1249/live15',
                         'outPutHttpFlow': 'http://10.78.64.195:1249/live15'},
                    15: {'id': '15', 'switchstatus': True, 'name': '移动直播16', 'programstatus': -1,
                         'outbandwidth': '1000', 'width': '960', 'height': '540',
                         'inPutFirst': 'http://61.49.160.199:8080/live/cct ', 'outPutFirst': 'udp://@228.1.2.145:1000',
                         'outPutSecond': 'http://10.78.64.195:1250/live16',
                         'outPutHttpFlow': 'http://10.78.64.195:1250/live16'},
                    16: {'id': '16', 'switchstatus': True, 'name': '移动直播17', 'programstatus': -1,
                         'outbandwidth': '1000', 'width': '960', 'height': '540',
                         'inPutFirst': 'rtmp://10.78.43.20/live/officecut01 ', 'outPutFirst': 'udp://@228.1.2.145:2000',
                         'outPutSecond': 'http://10.78.64.195:1251/live17',
                         'outPutHttpFlow': 'http://10.78.64.195:1251/live17'},
                    17: {'id': '17', 'switchstatus': True, 'name': '移动直播18', 'programstatus': -1,
                         'outbandwidth': '1000', 'width': '960', 'height': '540',
                         'inPutFirst': 'rtmp://59.110.126.141/live/CCTV12e5b1b1b16f644bdf9b972c9f13c3872aH ',
                         'outPutFirst': 'udp://@228.1.2.145:3000', 'outPutSecond': 'http://10.78.64.195:1252/live18',
                         'outPutHttpFlow': 'http://10.78.64.195:1252/live18'},
                    18: {'id': '18', 'switchstatus': True, 'name': '移动直播19', 'programstatus': -1,
                         'outbandwidth': '1000', 'width': '960', 'height': '540',
                         'inPutFirst': 'rtmp://59.110.127.144/live/CCTV2PGC1 ',
                         'outPutFirst': 'udp://@228.1.2.145:4000', 'outPutSecond': 'http://10.78.64.195:1253/live19',
                         'outPutHttpFlow': 'http://10.78.64.195:1253/live19'},
                    19: {'id': '19', 'switchstatus': True, 'name': '移动直播20', 'programstatus': -1,
                         'outbandwidth': '4000', 'width': '960', 'height': '540',
                         'inPutFirst': 'rtmp://vlive.people.com.cn/2010/1-18-11-29-1500/live_2 ',
                         'outPutFirst': 'udp://@228.1.2.145:5000', 'outPutSecond': 'http://10.78.64.195:1254/live20',
                         'outPutHttpFlow': 'http://10.78.64.195:1254/live20'}}

        tagMachine = Machine.objects.get(machineType__name='编码器')
        for key in messages.keys():
            # print(messages[key])
            # ProgramDetail.objects.filter(machine_id=1).create(**messages[key])
            # print(messages[key]['rowid'])
            ProgramDetail.objects.update_or_create(machine_id=tagMachine.id, **messages[key])
            # try:
            #     ProgramDetail.objects.get(machine=tagMachine, rowid=messages[key]['rowid'])
            # except ProgramDetail.DoesNotExist:
            #     ProgramDetail.objects.create(machine=tagMachine, **messages[key])
            # else:
            #     # print(ProgramDetail.objects.get(machine=tagMachine, rowid=messages[key]['rowid']))
            #     ProgramDetail.objects.get(machine=tagMachine, rowid=messages[key]['rowid']).(**messages[key])
            # ProgramDetail.objects.get_or_create(machine=tagMachine, rowid=messages[key]['rowid'])
            # ProgramDetail.objects.save()

    def reNewInfo(self):
        '''
        use check the target encoder data,update few data
        :return:
        '''
        pass



if __name__ == '__main__':

    def work():
        print('hello', os.getpid())
        from concurrent.futures import ThreadPoolExecutor as TPE
        def task(arg):
            time.sleep(0.5)
            print('Thread:', arg)
        pool = TPE(5)  # 线程池里放5个线程
        for i in range(100):
            # 去连接池中获取连接
            pool.submit(task, i)

    #part1:在主进程下开启多个线程,每个线程都跟主进程的pid一样
    t1=Thread(target=work)
    t2=Thread(target=work)
    t1.start()
    t2.start()
    print('主进程-->线程pid',os.getpid())

    #part2:开多个进程,每个进程都有不同的pid
    p1=Process(target=work)
    p2=Process(target=work)
    p1.start()
    p2.start()
    print('主进程-->子进程pid',os.getpid())