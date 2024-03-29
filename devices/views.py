from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from configureBaseData.models.devices import *
from configureBaseData.models.ips import *
from configureBaseData.models.venders import *
from configureBaseData.models.processes import *
from configureBaseData.models.ips import *
from configureBaseData.models.encoderserver import *
from django.forms.forms import pretty_name
from django.core.exceptions import ObjectDoesNotExist
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import Q
from django.db.models import Count
from django.template import RequestContext
import sys
import re, os
import xlrd
import xlwt
import json
from web_scan.web_auth import EncoderOperater
from web_scan.update import updateEncoder
from .forms import *
from django.contrib.auth.decorators import login_required
from excelTrigger.readExcel import readExcel
from unperdictableLiveFlowAssist.UPLFA import *
from django.core.exceptions import FieldError
from .monitorRoom.fabtools import fabAct
import fabric


# import datetime
def listAllDev(request):
    listAdminIP = IpV4.objects.filter(isHttpManage=True).select_related('MachineIp').all()
    return render(request, 'devices/listall.html', {'listDevice': listAdminIP})


def rebootDev(request):
    import devices.deviceOperater as operater
    listDevice = 'reboot'
    return render(request, 'devices/devices.html', {'listdevice': listDevice})


def detailDev(request):
    if request.method == 'GET':
        nid = int(request.GET.get('nid'))
        deviceInfo = Machine.objects.get(id=nid)
        deviceIp = IpV4.objects.filter(MachineIp=deviceInfo)
        deviceProcess = Process.objects.filter(runMachine=deviceInfo)
    elif request.method == 'POST':
        pass
    return render(request, 'devices/detail.html',
                  {'deviceInfo': deviceInfo, 'deviceIp': deviceIp, 'deviceProcess': deviceProcess})


@login_required
def encoders(request):
    '''

    :param request:
    :return:
    '''
    if request.method == 'GET':
        # query4 = ProgramDetail.objects.filter(machine__ipv4__isHttpManage='True',
        #                                       machine__machineType__name='编码器').order_by(
        #     'machine', 'rowid').values('name', 'machine__machineAssetNumber',
        #                                'machine__ipv4__ip', 'height', 'width', 'outPutHttpFlow', 'outPutFirst')
        queryEncoders = Machine.objects.filter(machineType__name='编码器', ipv4__isHttpManage='True').annotate(
            countip=Count("programdetail")).order_by('id', 'programdetail__rowid').values(
            'machineAssetNumber', 'programdetail__name', 'programdetail__height', 'programdetail__width',
            'programdetail__outPutSecond', 'ipv4__ip', 'programdetail__switchStatus',
            'programdetail__outPutFirst', 'programdetail__inPutSecond', 'programdetail__inPutFirst',
            'countip')
        # from web_scan import update
        # update.updateEncoderInfo()
        return render(request, 'encoders/listall.html', {'queryencoders': queryEncoders})
    elif request.method == 'POST':
        return None


def updateEncoders(request):
    if request.method == 'POST':
        queryEncoders = Machine.objects.filter(machineType__name='编码器', ipv4__isHttpManage='True').values('id',
                                                                                                          'httpadminp',
                                                                                                          'httpadmin',
                                                                                                          'ipv4__ip',
                                                                                                          'machineVender__englishname',
                                                                                                          )
        '''[{'id': , 'httpadminp': , 'httpadmin': , 'ipv4__ip': ,'machineVender__englishname': }]'''
        for items in queryEncoders:
            eor = EncoderOperater(ipadd=items['ipv4__ip'], username=items['httpadmin'],
                                  passwd=items['httpadminp'], targetType=items['machineVender__englishname'], )
            result = eor.doOption()
            updater = updateEncoder(machine=items['id'], messages=result)
            updater.updateInfo()
        return redirect('/devices/encoders')
    else:
        return None


@login_required
def staff(request):
    if request.method == 'POST':
        '''
        update value on the page
        '''
        # create a form instance and populate it with data from the request:
        getForm = StaffForm(request.POST)

        # check whether it's valid:
        if getForm.is_valid():
            department = getForm.cleaned_data['department']
            staffName = getForm.cleaned_data['staffName']
            phoneNumber = getForm.cleaned_data['phoneNumber']
            note = getForm.cleaned_data['note']
            Staff.objects.update_or_create(department=department, staffName=staffName, phoneNumber=phoneNumber,
                                           note=note)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('/tasks/staff')
            # return HttpResponseRedirect('tasks/listall.html', {'getForm': getForm})
    elif request.method == 'GET':
        message = Staff.objects.all().order_by('department')
        getForm = StaffForm()
        return render(request, 'tasks/staff.html', {'message': message, 'getForm': getForm})
    else:
        return HttpResponseRedirect('/thanks/')


@login_required
def staffDelete(request):
    if request.method == 'POST':
        sid = request.POST.get('sid')
        Staff.objects.filter(id=sid).delete()
        result = json.dumps({'sid': sid})
        return HttpResponse(result)
    else:
        return None


@login_required
def taskList(request):
    '''
    :param request:
    :return:
    '''

    if request.method == 'POST':
        '''
        update value on the page
        '''
        # create a form instance and populate it with data from the request:
        getForm = TaskForm(request.POST)
        # check whether it's valid:
        if getForm.is_valid():
            taskName = getForm.cleaned_data['taskName']
            startDate = getForm.cleaned_data['startDate']
            endDate = getForm.cleaned_data['endDate']
            typeOf = getForm.cleaned_data['typeOf']
            Task.objects.update_or_create(taskName=taskName, startDate=startDate, endDate=endDate, typeOf=typeOf)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('/tasks/listalltask')
            # return HttpResponseRedirect('tasks/listall.html', {'getForm': getForm})
    elif request.method == 'GET':
        message = Task.objects.all().reverse().annotate(countnum=Count('workpackage__programName')).values('taskName',
                                                                                                           'startDate',
                                                                                                           'endDate',
                                                                                                           'typeOf',
                                                                                                           'id',
                                                                                                           'countnum').order_by(
            '-startDate')
        getForm = TaskForm()
        return render(request, 'tasks/listall.html', {'message': message, 'getForm': getForm})
    else:
        return HttpResponseRedirect('/thanks/')


@login_required
def synctask(request):
    if request.method == 'POST':
        message = None
        try:
            syncFlowTable = syncTable()
            syncFlowTable.copyFile()
        except FileNotFoundError:
            return HttpResponse('文件无法复制，同步失败')
        try:
            syncFlowTable.liveSteam()
            syncFlowTable.qSteam()
        except FieldError:
            message = 'django出错,单元格有问题,同步失败'
        except Exception as e:
            raise e
            # message = '清流表有问题，同步失败'
        if message:
            return HttpResponse(message)
        return HttpResponse('同步成功')
    else:
        return HttpResponse('error')


@login_required
def workPakgeList(request):
    if request.method == 'GET':
        searchId = request.GET.get('tid')
        message = WorkPackage.objects.filter(task__pk=searchId).values('id', 'programName', 'startDate', 'endDate',
                                                                       'isLive', 'isRecode', 'programChannel',
                                                                       'inPutStream', 'adminStaff__staffName',
                                                                       'notes').order_by('-startDate')

        getForm = WorkPackageForm(initial={'task': searchId})
        getForm.task = searchId

        return render(request, 'tasks/detail.html', {'message': message, 'getForm': getForm, 'tid': searchId})
    elif request.method == 'POST':
        '''
        update value on the page
        '''
        # create a form instance and populate it with data from the request:
        getForm = WorkPackageForm(request.POST)
        # check whether it's valid:
        if getForm.is_valid():
            task = getForm.cleaned_data['task']
            startDate = getForm.cleaned_data['startDate']
            endDate = getForm.cleaned_data['endDate']
            programChannel = getForm.cleaned_data['programChannel']
            programName = getForm.cleaned_data['programName']
            inPutStream = getForm.cleaned_data['inPutStream']
            isLive = getForm.cleaned_data['isLive']
            isRecode = getForm.cleaned_data['isRecode']
            notes = getForm.cleaned_data['notes']
            adminStaff = getForm.cleaned_data['adminStaff']
            taskId = Task.objects.get(id=task)
            WorkPackage.objects.update_or_create(task=taskId, startDate=startDate, endDate=endDate,
                                                 programChannel=programChannel,
                                                 programName=programName, inPutStream=inPutStream, isLive=isLive,
                                                 isRecode=isRecode, notes=notes, adminStaff=adminStaff)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            returnUrl = '/tasks/detailwork?tid=' + str(task)
            return HttpResponseRedirect(returnUrl)


@login_required
def workPakgeListDelete(request):
    if request.method == 'POST':
        tid = request.POST.get('tid')
        wid = request.POST.get('wid')
        WorkPackage.objects.filter(task=tid, pk=wid).delete()
        result = json.dumps({'wid': wid})
        return HttpResponse(result)
    else:
        return None


def workDaily(request):
    if request.method == 'GET':
        searchStartTime = request.GET.get('starttime')
        searchEndTime = request.GET.get('endtime')
        # searchField = request.GET.get('searchfield')
        '''
        get the datetime
        '''
        if searchStartTime:
            searchEndTime = str(searchEndTime)
            searchStartTime = str(searchStartTime)
            # searchField = int(searchField)
            searchStartTime = datetime.datetime.strptime(searchStartTime, '%Y-%m-%d')
            searchStartTime = datetime.datetime(searchStartTime.year, searchStartTime.month,
                                                searchStartTime.day, 00,
                                                00, 00)
            searchEndTime = datetime.datetime.strptime(searchEndTime, '%Y-%m-%d')
            searchEndTime = datetime.datetime(searchEndTime.year, searchEndTime.month, searchEndTime.day, 23,
                                              59, 59)
        # if searchField == 0:
        #     message = WorkPackage.objects.filter(startDate__range=(searchStartTime, searchEndTime))
        # elif searchField == 1:
        #     message = WorkPackage.objects.filter(updata_time__range=(searchStartTime, searchEndTime))
        else:
            today = datetime.datetime.now()
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            search_today = today
            searchStartTime = datetime.datetime(search_today.year, search_today.month, search_today.day, 00, 00, 00)
            search_today_end = datetime.datetime(search_today.year, search_today.month, search_today.day, 23, 59, 59)
            searchEndTime = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59)
        message = WorkPackage.objects.filter(startDate__range=(searchStartTime, searchEndTime))
        # searchStartTime = today
        # searchEndTime = tomorrow
        '''
        count the number 
        '''
        messageCount = message.aggregate(Count('id'))
        dictCount = 0
        messagedict = dict()
        for item in message.values('id', 'startDate', 'endDate', 'programChannel', 'programName', 'inPutStream',
                                   'isLive', 'isRecode', 'adminStaff__staffName', 'adminStaff__department'):

            # taskMessage = item.values('id', 'startDate', 'endDate', 'programChannel', 'programName', )
            programMessage = ProgramDetail.objects.filter(name=item['programChannel']).values('programStatus',
                                                                                              'inPutFirst',
                                                                                              'outPutHttpFlow')
            if programMessage:
                for subitem in programMessage:
                    messagedict[dictCount] = item
                    messagedict[dictCount].update(subitem)
            else:
                messagedict[dictCount] = item
            dictCount = dictCount + 1

    return render_to_response('tasks/daily.html',
                              {'message': messagedict, 'messageCount': messageCount, 'today': searchStartTime,
                               'tomorrow': searchEndTime, })


def getEncoderStatus(request):
    if request.method == 'GET':
        '''
        get id,time,programChannel,
        :return id, program status
        '''
        today = datetime.datetime.now()
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        search_today = today
        searchStartTime = datetime.datetime(search_today.year, search_today.month, search_today.day, 00, 00, 00)
        search_today_end = datetime.datetime(search_today.year, search_today.month, search_today.day, 23, 59, 59)
        searchEndTime = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59)
        workPackageMessage = WorkPackage.objects.filter(startDate__range=(searchStartTime, searchEndTime))
        workPackageDict = dict()
        machineDict = dict()
        for item in workPackageMessage.values('id', 'programChannel', ):

            programMessage = ProgramDetail.objects.filter(name=item['programChannel']).values(
                'rowid', 'machine_id', )
            for item in programMessage:
                if item['machine_id'] in machineDict:
                    machineDict[item['machine_id']].append(item['rowid'])
                else:
                    machineDict[item['machine_id']] = list()
                    machineDict[item['machine_id']].append(item['rowid'])
        pass
        '''{1: [0, 7]}'''
        for key in machineDict:
            targetMachine = Machine.objects.filter(id=key, ipv4__isHttpManage=True).values('id', 'ipv4__ip',
                                                                                           'httpadmin', 'httpadminp', )

            eor = EncoderOperater(ipadd=targetMachine[0]['ipv4__ip'], username=targetMachine[0]['httpadmin'],
                                  passwd=targetMachine[0]['httpadminp'], targetType='realmagic', rawid=machineDict[key])
            result = eor.doOption()
            updater = updateEncoder(machine=targetMachine[0]['id'], messages=result)
            updater.updateInfo()
        returnMessage = WorkPackage.objects.filter(startDate__range=(searchStartTime, searchEndTime))
        returnMessageList = list()
        for item in returnMessage.values('id', 'programChannel', ):
            programMessage = ProgramDetail.objects.filter(name=item['programChannel']).values('programStatus',
                                                                                              'inPutFirst',
                                                                                              'outPutHttpFlow')

            programstatus = lambda x: '有流' if x > 0 else '无流'
            returnMessageList.append(
                {'wid': item['id'], 'programstatus': programstatus(programMessage[0]['programStatus']),
                 'inPutFirst': programMessage[0]['inPutFirst'], 'outPutHttpFlow': programMessage[0]['outPutHttpFlow']})
            # print(returnMessageDict)

        return HttpResponse(json.dumps(returnMessageList))
        # return redirect("/tasks/daily")
    else:
        return HttpResponse(None)


def exportTaskExcel(request):
    if request.method == 'GET':
        searchStartTime = request.GET.get('starttime')
        searchEndTime = request.GET.get('endtime')
        if searchStartTime:
            searchEndTime = str(searchEndTime)
            searchStartTime = str(searchStartTime)
            searchStartTime = datetime.datetime.strptime(searchStartTime, '%Y-%m-%d')
            searchStartTime = datetime.datetime(searchStartTime.year, searchStartTime.month,
                                                searchStartTime.day, 00,
                                                00, 00)
            searchEndTime = datetime.datetime.strptime(searchEndTime, '%Y-%m-%d')
            searchEndTime = datetime.datetime(searchEndTime.year, searchEndTime.month, searchEndTime.day, 23,
                                              59, 59)
            message = WorkPackage.objects.filter(startDate__range=(searchStartTime, searchEndTime)).values(
                'startDate',
                'task__taskName',
                'adminStaff__staffName',
                'adminStaff__department',
                'isRecode',
                'isLive',
                'notes',
                'inPutStream',
                'programChannel',
                'endDate',
                'programName', )

            activity_list = message.aggregate(Count('id'))
            response = HttpResponse(content_type="application/ms-excel")
            response['Content-Disposition'] = 'attachment; filename=file.xls'

            wb = xlwt.Workbook()
            ws = wb.add_sheet('Sheetname')
            icon = 1
            dateFormat = xlwt.XFStyle()
            dateFormat.num_format_str = 'yyyy/mm/dd hh:mm'
            list_title = [u'开始日期', u'开始时间', u'结束日期', u'结束时间', u'节目名称', u'需求部门', u'源地址', u'使用频道', u'负责人', u'收录',
                          u'直播',
                          u'备注']
            for i in range(0, len(list_title)):
                '''
                wirte excel title
                '''
                ws.write(0, i, list_title[i])
            for infor in message:
                '''
                get data from workpackage and task write 
                task,startDate,endDate,programChannel,programStatus,programName,inPutStream,notes,adminStaff
                to excel and download it
                '''
                plan_start_day = infor['startDate'].replace(tzinfo=None)
                plan_start_day = plan_start_day + datetime.timedelta(hours=8)
                plan_start_time = plan_start_day.strftime('%H:%m')
                ws.write(icon, 0, plan_start_day.strftime('%Y/%m/%d'), dateFormat)
                ws.write(icon, 1, plan_start_time, dateFormat)
                plan_end_day = infor['endDate'].replace(tzinfo=None)
                plan_end_day = plan_end_day + datetime.timedelta(hours=8)
                plan_end_time = plan_end_day.strftime('%H:%m')
                ws.write(icon, 2, plan_end_day.strftime('%Y/%m/%d'), dateFormat)
                ws.write(icon, 3, plan_end_time, dateFormat)
                ws.write(icon, 4, infor['programName'])
                ws.write(icon, 5, infor['adminStaff__department'])
                ws.write(icon, 6, infor['inPutStream'])
                ws.write(icon, 7, infor['programChannel'])
                ws.write(icon, 8, infor['adminStaff__staffName'])
                ws.write(icon, 9, infor['isRecode'])
                ws.write(icon, 10, infor['isLive'])
                ws.write(icon, 11, infor['notes'])
                icon += 1
            wb.save(response)
            return response


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def inportTaskExcel(request):
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     handle_uploaded_file(request.FILES['file'])
        #     return HttpResponseRedirect('/success/url/')
        obj = request.FILES.get('importfile')
        if not obj:
            return HttpResponse('不能提交空表格')
        file_path = os.path.join('static', 'upload', obj.name)
        f = open(file_path, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        getInportObj = readExcel(filepath=file_path, filename=obj.name)
        objDict = getInportObj.typeOfExcel()

        for item in objDict:
            if item == 0:
                continue
            # print(objDict[item])
            firstsell = re.split('/', objDict[item][0])
            secondsell = re.split(':', objDict[item][1])
            thirdsell = re.split('/', objDict[item][2])
            fourthsell = re.split(':', objDict[item][3])
            startdate = datetime.datetime(int(firstsell[0]), int(firstsell[1]), int(firstsell[2]),
                                          int(secondsell[0]),
                                          int(secondsell[1]))
            enddate = datetime.datetime(int(thirdsell[0]), int(thirdsell[1]), int(thirdsell[2]), int(fourthsell[0]),
                                        int(fourthsell[1]))
            Task.objects.get_or_create(taskName=objDict[item][4])
            Staff.objects.get_or_create(department=objDict[item][8], staffName=objDict[item][9])
            WorkPackage.objects.create(
                startDate=startdate,
                endDate=enddate,
                programName=objDict[item][5],
                programChannel=objDict[item][7],
                inPutStream=objDict[item][6],
                isRecode=objDict[item][10],
                isLive=objDict[item][11],
                notes=objDict[item][12],
                task=Task.objects.get(taskName=objDict[item][4]),
                adminStaff=Staff.objects.get(department=objDict[item][8], staffName=objDict[item][9]),
            )
        # # # print obj.name ,obj.size
        return redirect('/tasks/inportworks')
    elif request.method == 'GET':
        return render(request, 'tasks/inportexcel.html')


def machineroom(request):
    if request.method == 'GET':
        message = MachineRoom.objects.all().annotate(countnum=Count('machinerack')).values('name', 'address',
                                                                                           'note',
                                                                                           'countnum')
        return render(request, 'machinerooms/listall.html', {'message': message, })
    elif request.method == 'POST':
        '''
        update value on the page
        '''
        # create a form instance and populate it with data from the request:
        getForm = WorkPackageForm(request.POST)
        # check whether it's valid:
        if getForm.is_valid():
            return HttpResponse('404')
            # return HttpResponseRedirect(returnUrl)


@login_required
def livechina(request):
    if request.method == 'GET':
        return render(request, 'livechina/listall.html', )
    elif request.method == 'POST':
        return render(request, 'livechina/listall.html', )


@login_required
def monitorroom(request):
    if request.method == 'GET':
        result = Machine.objects.filter(services__name='VSMplayer').values('id', 'ipv4__ip', 'services__name').order_by(
            'ipv4__ip')
        # from .monitorRoom.VSMplayerAss import vsm
        # result2 = vsm.check
        return render(request, 'mointorRoom/listall.html', {'result': result})
    elif request.method == 'POST':
        nid = request.POST.get('nid')
        action_value = request.POST.get('value')
        action_object = Machine.objects.filter(id=nid).values('ipv4__ip', 'loginUser', 'loginPass')
        print(action_object.first()['ipv4__ip'])

        actionTag = fabAct(host=action_object.first()['ipv4__ip'], port=22, username=action_object.first()['loginUser'],
                           passwd=action_object.first()['loginPass'], )
        if action_value == 'restart':
            actionTag.rebootDev()
        elif action_value == 'restartp':
            actionTag.restartProcess()
        elif action_value == 'shutdown':
            actionTag.shutDownDev()
        return render(request, 'mointorRoom/listall.html', )


'''
def change_status_flow(request):
    if request.method=='POST':
        nid = int(request.POST.get('nid'))
        chang_obj=video_flow.objects.filter(id=nid)
        for status in chang_obj:
            change_id = status.program_status + 1

        if change_id >3:
            change_id = 0

        chang_obj.update(program_status=change_id)
        for sta in chang_obj:
            req =  sta.get_program_status_display()

        return HttpResponse(req)

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def flowlistimport(request):
    if request.method == 'POST':
        obj = request.FILES.get('importfile')
        if not obj:
            return HttpResponse('不能提交空表格')
        file_path = os.path.join('static','upload',obj.name)
        f = open(file_path,'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        xldata = xlrd.open_workbook(file_path)
        xltable = xldata.sheets()[0]
        nrows= xltable.nrows
        deparment_dict= {u'体育中心':'0',
        u'微视频工作室':'1',
        u'少儿社区部':'2',
        u'央视新闻':'3',
        u'综艺社区部':'4',
        u'网络媒体事业部':'5',
        u'品牌部':'6',
        u'国际传播事业部':'7',u'国际传播事业群':'7',
        u'舆论场':'8',
        u'CGTN':'9',
        u'科教纪录中心':'10'}
        use_for_dict = [
            u'审核',
            u'收录',
            u'审核/收录',
            u'CGTN直播',
            u'CGTN电视',
        ]
        source_addr_dict={
            u'互动1': 'http://192.168.169.12:8088/yuxuan1',
            u'互动2': 'http://192.168.169.12:8088/yuxuan2',
            u'互动3': 'http://192.168.169.12:8088/yuxuan3',
            u'互动4': 'http://192.168.169.12:8088/yuxuan4',
            u'互动5': 'http://192.168.169.12:8088/yuxuan5',
            u'互动6': 'http://192.168.169.12:8088/yuxuan6',
            u'互动7': 'http://192.168.169.12:8088/yuxuan7',
            u'互动8': 'http://192.168.169.12:8088/yuxuan8',
            u'互动9': 'http://192.168.169.12:8088/yuxuan9',
            u'互动10': 'http://192.168.169.12:8088/yuxuan10',
            u'冬奥01':'http://192.168.169.12:8088/ss1',
            u'冬奥02': 'http://192.168.169.12:8088/ss2',
            u'冬奥03': 'http://192.168.169.12:8088/ss3',
            u'冬奥04': 'http://192.168.169.12:8088/ss4',
            u'冬奥05': 'http://192.168.169.12:8088/ss5',
            u'冬奥06': 'http://192.168.169.12:8088/ss6',
            u'冬奥07': 'http://192.168.169.12:8088/ss7',
            u'冬奥体育01': 'http://192.168.169.12:8088/ss7',
            u'冬奥08': 'http://192.168.169.12:8088/ss8',
            u'冬奥体育02': 'http://192.168.169.12:8088/ss8',
            u'冬奥09': 'http://192.168.169.12:8088/ss9',
            u'冬奥10': 'http://192.168.169.12:8088/ss10',
            u'冬奥11': 'http://192.168.169.12:8088/ss11',
            u'冬奥12': 'http://192.168.169.12:8088/ss12',
            u'冬奥13': 'http://192.168.169.12:8088/ss13',
            u'冬奥14': 'http://192.168.169.12:8088/ss14',
            u'冬奥15': 'http://192.168.169.12:8088/ss15',
            u'冬奥16': 'http://192.168.169.12:8088/ss16',
            u'冬奥17': 'http://192.168.169.12:8088/ss17',
            u'冬奥18': 'http://192.168.169.12:8088/ss18',
            u'冬奥19': 'http://192.168.169.12:8088/ss19',
            u'冬奥20': 'http://192.168.169.12:8088/ss20',
        }
        tunnel_dict = {
            u'体育01':'1',
            u'冬奥体育01':'1',
            u'体育02':'2',
            u'冬奥体育02': '2',
            u'体育03':'3',
            u'体育04':'4',
            u'体育05':'5',
            u'体育06':'6',
            u'体育07':'7',
            u'体育08':'8',
            u'体育09':'9',
            u'体育10':'10',
            u'互动1': '1',
            u'互动2': '2',
            u'互动3': '3',
            u'互动4': '4',
            u'互动5': '5',
            u'互动6': '6',
            u'互动7': '7',
            u'互动8': '8',
            u'互动9': '9',
            u'互动10': '10',
            u'移动直播01':'11',u'LIVE01':'11',
            u'移动直播02':'12',u'LIVE02':'12',
            u'移动直播03':'13',u'LIVE03':'13',
            u'移动直播04':'14',u'LIVE04':'14',
            u'移动直播05':'15',u'LIVE05':'15',
            u'移动直播06':'16',u'LIVE06':'16',
            u'移动直播07':'17',u'LIVE07':'17',
            u'移动直播08':'18',u'LIVE08':'18',
            u'移动直播09':'19',u'LIVE09':'19',
            u'移动直播10':'20',u'LIVE10':'20',
            u'移动直播11':'21',u'LIVE11':'21',
            u'移动直播12':'22',u'LIVE12':'22',
            u'移动直播13':'23',u'LIVE13':'23',
            u'移动直播14':'24',u'LIVE14':'24',
            u'移动直播15':'25',u'LIVE15':'25',
            u'移动直播16':'26',u'LIVE16':'26',
            u'移动直播17':'27',u'LIVE17':'27',
            u'移动直播18':'28',u'LIVE18':'28',
            u'移动直播19':'29',u'LIVE19':'29',
            u'移动直播20':'30',u'LIVE20':'30',

            u'switch01':'31',
            u'switch02':'32',
            u'switch03':'33',
            u'switch04':'34',}
        if '移动直播' in obj.name :
            # print obj.name
            # return HttpResponse('ok')
            for i in range(nrows):

                firstsell = xlrd.xldate_as_datetime(xltable.row_values(i)[1],0)
                secondsell = xltable.row_values(i)[3].replace('：',':')
                secondsell = secondsell.replace('——', '-')
                secondsell = secondsell.replace('—','-')
                secondsell = re.split(r'-',secondsell)

                fisttime = secondsell[0].split(':')
                secondtime = secondsell[1].split(':')
                startdate = datetime.datetime(firstsell.year,firstsell.month,firstsell.day,hour=int(fisttime[0]),minute=int(fisttime[1]))

                enddate = datetime.datetime(firstsell.year,firstsell.month,firstsell.day,hour=int(secondtime[0]),minute=int(secondtime[1]))

                source_addr = xltable.row_values(i)[13]
                if xltable.row_values(i)[10] in tunnel_dict.keys():
                    tunnel_addr = tunnel_dict[xltable.row_values(i)[10]]
                else:
                    tunnel_addr = xltable.row_values(i)[10]

                video_flow.objects.create(plan_start_date=startdate,
                                          plan_end_date=enddate,
                                          program_name =  xltable.row_values(i)[2],
                                          department = deparment_dict[xltable.row_values(i)[4]],
                                          admin_name = xltable.row_values(i)[6],
                                          source_addr=source_addr,
                                          video_id =xltable.row_values(i)[14],

                                          tunnel=tunnel_addr,

                                          notes = xltable.row_values(i)[16],
                                          use_for=2,

                )
            # # print obj.name ,obj.size
            return redirect('/list/flowlistimport')
        else:
            for i in range(nrows):
                if i == 0:
                    continue
                firstsell = xlrd.xldate_as_datetime(xltable.row_values(i)[0],0)
                secondsell = xlrd.xldate_as_datetime(xltable.row_values(i)[1],0)
                thirdsell = xlrd.xldate_as_datetime(xltable.row_values(i)[2],0)
                fourthsell = xlrd.xldate_as_datetime(xltable.row_values(i)[3],0)
                startdate = datetime.datetime(firstsell.year,firstsell.month,firstsell.day,secondsell.hour,secondsell.minute)

                enddate = datetime.datetime(thirdsell.year,thirdsell.month,thirdsell.day,fourthsell.hour,fourthsell.minute)
                if xltable.row_values(i)[6] in source_addr_dict.keys():
                    source_addr=source_addr_dict[xltable.row_values(i)[6]]
                else:
                    source_addr = xltable.row_values(i)[6]
                if xltable.row_values(i)[6] in tunnel_dict.keys():
                    tunnel_addr = tunnel_dict[xltable.row_values(i)[6]]
                else:
                    tunnel_addr = xltable.row_values(i)[6]
                if len(xltable.row_values(i))>=11:
                    write_notes = xltable.row_values(i)[10]
                else:
                    write_notes = None
                #print startdate,enddate,xltable.row_values(i)[4]
                video_flow.objects.create(plan_start_date=startdate,
                                          plan_end_date=enddate,
                                          program_name =  xltable.row_values(i)[4],
                                          department = deparment_dict[xltable.row_values(i)[5]],
                                          admin_name = xltable.row_values(i)[8],
                                          source_addr=source_addr,
                                          video_id =xltable.row_values(i)[7],

                                          tunnel=tunnel_addr,
                                          use_for=use_for_dict.index(xltable.row_values(i)[9]),
                                          notes = write_notes,
                )
            # print obj.name ,obj.size
            return redirect('/list/flowlistimport')
    elif request.method == 'GET':
        return  render(request,'video_flow_import.html')
def multi_getattr(obj, attr, default=None):
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj

def get_column_head(obj, name):
    name = name.rsplit('.', 1)[-1]
    return pretty_name(name)

def get_column_cell(obj, name):
    try:
        attr = multi_getattr(obj, name)
    except ObjectDoesNotExist:
        return None
    if hasattr(attr, '_meta'):
        # A Django Model (related object)
        return unicode(attr).strip()
    elif hasattr(attr, 'all'):
        # A Django queryset (ManyRelatedManager)
        return ', '.join(unicode(x).strip() for x in attr.all())
    return attr
'''
