from excelTrigger.readExcel import readExcel
import os
import time
import re
import datetime

path = os.path.abspath('移动直播2019年.xls')
filename = '移动直播2019年.xls'
# print(path)
obj = readExcel(filepath=path, filename=filename, sheetname='直播明细')
obj2 = readExcel(filepath=path, filename=filename, sheetname='纯清流')
objDict = obj.typeOfExcel()
for item in objDict:
    if item == 0:
        continue
    # print(objDict[item][1], time.localtime(objDict[item][2] + 1546574130.0), objDict[item][3])
    dateSerial = objDict[item][2]
    dateSeconds = (dateSerial - 25569) * 86400.0
    startDate = datetime.datetime.utcfromtimestamp(dateSeconds)
    # time.localtime(objDict[item][2] + 1547438126.0)
    timeRange = re.split('[-——]', objDict[item][3])
    startTime = datetime.datetime.strptime(timeRange[0], '%H:%M')
    endTime = datetime.datetime.strptime(timeRange[1], '%H:%M')
    startDatetime = datetime.datetime(startDate.year, startDate.month, startDate.day, hour=startTime.hour,
                                      minute=startTime.minute)
    endDatetime = datetime.datetime(startDate.year, startDate.month, startDate.day, hour=endTime.hour,
                                    minute=endTime.minute)

    isLive = objDict[item][6]
    isRecode = objDict[item][8]
    programChannel = objDict[item][5]
    source = objDict[item][15]
    print('----')
    if '\n' in source:
        source = re.sub('[主:|备:|主：|备：|主|备]', '', source)
        listone = re.split('\n', source)
        inPutStream = listone[0]
        inPutStreamSub = listone[1]
    else:
        inPutStream = source
        inPutStreamSub = None
    programName = objDict[item][4]

    if item > 5:
        break
    taskName = re.split('.', filename)[0]
    # Task.objects.get_or_create(taskName=objDict[item][4])
    # Staff.objects.get_or_create(department=objDict[item][8], staffName=objDict[item][9])
    # WorkPackage.objects.create(
    startDate = startDate,
    endDate = endDatetime,
    programName = programName,
    programChannel = programChannel,
    inPutStream = inPutStream,
    inPutStreamSub = inPutStreamSub,
    isRecode = isRecode,
    isLive = isLive,
    notes = objDict[item][12],
    # task=Task.objects.get(taskName=objDict[item][4]),
    # adminStaff=Staff.objects.get(department=objDict[item][8], staffName=objDict[item][9]),
# )

# print(time.localtime(43474.0 + 1547438126.0))
# print(time.time(2019/1/5))
# print(time.time(datetime.date(9999, 12, 31)))
# print(datetime.date.(datetime.date(2005, 7, 8)))
dt = "2019-01-5 0:0:0"
dt2 = "2019-01-5 0:0:3"

# 转换成时间数组
timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
timeArray2 = time.strptime(dt2, "%Y-%m-%d %H:%M:%S")
# 转换成时间戳
timestamp = time.mktime(timeArray)
timestamp2 = time.mktime(timeArray2)
# print(timestamp - timestamp2)
