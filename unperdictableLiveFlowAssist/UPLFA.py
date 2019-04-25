from excelTrigger.readExcel import readExcel
import os
import time
import re
import datetime
from configureBaseData.models import Task, WorkPackage, Staff

class syncTable(object):
    def __init__(self):
        self.path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '移动直播2019年.xls')
        self.filename = '移动直播2019年.xls'
    def liveSteam(self):
        # print(path)
        obj = readExcel(filepath=self.path, filename=self.filename, sheetname='直播明细')
        objDict = obj.typeOfExcel()
        for item in objDict:
            if item == 0:
                continue
            programName = objDict[item][4]
            # print(programName)
            if len(programName) < 5:
                continue
            # print(objDict[item][1], time.localtime(objDict[item][2] + 1546574130.0), objDict[item][3])
            dateSerial = objDict[item][2]
            dateSeconds = (dateSerial - 25569) * 86400.0
            startDate = datetime.datetime.utcfromtimestamp(dateSeconds)
            # time.localtime(objDict[item][2] + 1547438126.0)
            startTime=None
            if len(objDict[item][3])<3:
                startTime = 'blank'
            elif re.search('\n', objDict[item][3]):
                # print(objDict[item][3])
                timeBlock = re.split('\n', objDict[item][3])
                # print(timeBlock)
                timeFirstBlock = re.split('[-——]', timeBlock[0])
                timeSecondBlock = re.split('[-——]', timeBlock[1])
                timeRange = [timeFirstBlock[0],timeSecondBlock[1]]
                # print(timeRange)
            else:
                timeRange = re.split('[-——]', objDict[item][3])
            if startTime:
                startDatetime=None
                endDatetime=None
            else:
                startTime = datetime.datetime.strptime(timeRange[0], '%H:%M')
                try:
                    endTime = datetime.datetime.strptime(timeRange[1], '%H:%M')
                except ValueError:
                    endTime = timeRange[1].replace('24', '00')
                    endTime = datetime.datetime.strptime(endTime, '%H:%M')
                startDatetime = datetime.datetime(startDate.year, startDate.month, startDate.day, hour=startTime.hour,
                                                  minute=startTime.minute)
                endDatetime = datetime.datetime(startDate.year, startDate.month, startDate.day, hour=endTime.hour,
                                                minute=endTime.minute)

            isLive = objDict[item][6]
            isRecode = objDict[item][8]
            programChannel = objDict[item][5]
            source = objDict[item][15]
            if '\n' in source:
                source = re.sub('[主:|备:|主：|备：|主|备]', '', source)
                listone = re.split('\n', source)
                inPutStream = listone[0]
                inPutStreamSub = listone[1]
            else:
                inPutStream = source
                inPutStreamSub = None
            programName = objDict[item][4]

            # if item > 5:
            #     break
            taskName = '移动直播2019年'
            staffName = objDict[item][10]
            department = objDict[item][12]
            Task.objects.get_or_create(taskName=taskName)
            Staff.objects.get_or_create(department=department, staffName=staffName)
            WorkPackage.objects.create(
                startDate=startDate,
                endDate=endDatetime,
                programName=programName,
                programChannel=programChannel,
                inPutStream=inPutStream,
                inPutStreamSub=inPutStreamSub,
                isRecode=isRecode,
                isLive=isLive,
                # notes = objDict[item][12],
                task=Task.objects.get(taskName=taskName),
                adminStaff=Staff.objects.get(department=department, staffName=staffName),
            )

        # print(time.localtime(43474.0 + 1547438126.0))
        # print(time.time(2019/1/5))
        # print(time.time(datetime.date(9999, 12, 31)))
        # print(datetime.date.(datetime.date(2005, 7, 8)))
        '''
        dt = "2019-01-5 0:0:0"
        dt2 = "2019-01-5 0:0:3"
        
        # 转换成时间数组
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        timeArray2 = time.strptime(dt2, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        timestamp2 = time.mktime(timeArray2)
        # print(timestamp - timestamp2)
        '''
    def qSteam(self):
        obj2 = readExcel(filepath=self.path, filename=self.filename, sheetname='纯清流')
