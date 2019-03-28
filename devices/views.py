from django.shortcuts import render
# from django.http import HttpResponse
from configureBaseData.models.devices import *
from configureBaseData.models.ips import *
from configureBaseData.models.venders import *
from configureBaseData.models.processes import *
from configureBaseData.models.ips import *


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
        deviceProcess = Process.objects.filter(runMachine=deviceInfo)
    elif request.method=='POST':
        pass

    # print(deviceProcess.query)
    return render(request, 'devices/detail.html', {'deviceInfo': deviceInfo, 'deviceIp': deviceIp,'deviceProcess':deviceProcess})
from configureBaseData.models.encoderserver import *

def encoders(request):
    if request.method=='GET':
        # query1 = IpV4.objects.filter(isManage='True')
        # query2 = query1.Machine.id
        # query3 = Machine.objects.filter(ipv4__isManage='True',machine_type__name='1')
        query4 = ProgramDetail.objects.filter(machine__ipv4__isManage='True',machine__machine_type__name='1').order_by('machine','rowid').values('name','machine__machine_asset_number',
                                                                                                                     'machine__ipv4__ip')
        # query5 = Machine.objects.filter(query4)
        from web_scan import update
        update.updateEncoderInfo()
        # print('test')
        # for i in query4:
        #     print(i)
        return render(request,'encoders/listall.html',{'programlist':query4})

def taskList(request):
    if request.method == 'GET':
        search_start_time = request.GET.get('starttime')
        search_end_time = request.GET.get('endtime')
        search_field = request.GET.get('searchfield')
        if search_field:
            search_end_time = str(search_end_time)
            search_start_time = str(search_start_time)
            search_field = int(search_field)
            search_start_time = datetime.datetime.strptime(search_start_time, '%Y-%m-%d')
            search_start_time = datetime.datetime(search_start_time.year, search_start_time.month,
                                                  search_start_time.day, 00,
                                                  00, 00)
            search_end_time = datetime.datetime.strptime(search_end_time, '%Y-%m-%d')
            search_end_time = datetime.datetime(search_end_time.year, search_end_time.month, search_end_time.day, 23,
                                                59, 59)
        if search_field == 0:
            message = video_flow.objects.filter(plan_start_date__range=(search_start_time, search_end_time))
        elif search_field == 1:
            message = video_flow.objects.filter(updata_time__range=(search_start_time, search_end_time))
        else:
            today = datetime.datetime.now()
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            search_today = today
            search_today = datetime.datetime(search_today.year, search_today.month, search_today.day, 00, 00, 00)
            search_today_end = datetime.datetime(search_today.year, search_today.month, search_today.day, 23, 59, 59)
            search_tomorrow = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59)
            message = video_flow.objects.filter(plan_start_date__range=(search_today, search_tomorrow))
            message_count = video_flow.objects.filter(
                plan_start_date__range=(search_today, search_today_end)).aggregate(Count('id'))
            search_start_time = today
            search_end_time = tomorrow
    message_count = message.aggregate(Count('id'))
    return render_to_response('video_flow_list.html',
                              {'message': message, 'message_count': message_count, 'today': search_start_time,
                               'tomorrow': search_end_time, 'search_field': search_field})
def flowlistexport(request):
    if request.method == 'GET':
        search_start_time = request.GET.get('starttime')
        search_end_time = request.GET.get('endtime')
        if search_start_time:
            search_end_time = str(search_end_time)
            search_start_time = str(search_start_time)
            search_start_time = datetime.datetime.strptime(search_start_time, '%Y-%m-%d')
            search_start_time = datetime.datetime(search_start_time.year, search_start_time.month,
                                                  search_start_time.day, 00,
                                                  00, 00)
            search_end_time = datetime.datetime.strptime(search_end_time, '%Y-%m-%d')
            search_end_time = datetime.datetime(search_end_time.year, search_end_time.month, search_end_time.day, 23,
                                                59, 59)
            message = video_flow.objects.filter(plan_start_date__range=(search_start_time, search_end_time))
            activity_list = message.aggregate(Count('id'))
            response = HttpResponse(content_type="application/ms-excel")
            response['Content-Disposition'] = 'attachment; filename=file.xls'

            wb = xlwt.Workbook()
            ws = wb.add_sheet('Sheetname')
            icon = 1
            dateFormat = xlwt.XFStyle()
            dateFormat.num_format_str = 'yyyy/mm/dd hh:mm'
            list_taitle=[u'开始日期',u'开始时间',u'结束日期',u'结束时间',u'节目名称',u'需求部门',u'源地址',u'输出地址',u'负责人',u'用途',u'备注']
            for i in range(0,len(list_taitle)):
                ws.write(0,i,list_taitle[i])
            for infor in message:
                plan_start_day =  infor.plan_start_date.replace(tzinfo=None)
                plan_start_day=plan_start_day + datetime.timedelta(hours=8)
                plan_start_time = plan_start_day.strftime('%H:%m')
                ws.write(icon, 0, plan_start_day.strftime('%Y/%m/%d'),dateFormat)
                ws.write(icon, 1,plan_start_time,dateFormat)
                plan_end_day = infor.plan_end_date.replace(tzinfo=None)
                plan_end_day = plan_end_day + datetime.timedelta(hours=8)
                plan_end_time = plan_end_day.strftime('%H:%m')
                ws.write(icon, 2, plan_end_day.strftime('%Y/%m/%d'),dateFormat)
                ws.write(icon, 3,plan_end_time,dateFormat)
                ws.write(icon, 4, infor.program_name)
                ws.write(icon, 5, infor.get_department_display())
                ws.write(icon, 6,infor.source_addr)
                ws.write(icon, 7,infor.video_id)
                ws.write(icon, 8, infor.admin_name)
                ws.write(icon, 9, infor.get_use_for_display())
                ws.write(icon, 10, infor.notes)
                icon += 1
            wb.save(response)
            return response

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

def faq_form(request):
    if request.method == 'GET':
        search_start_time = request.GET.get('starttime')
        search_end_time = request.GET.get('endtime')
        print search_start_time, search_end_time
        if search_start_time:
            search_end_time = str(search_end_time)
            search_start_time = str(search_start_time)
            search_start_time = datetime.datetime.strptime(search_start_time, '%Y-%m-%d')
            search_start_time = datetime.datetime(search_start_time.year, search_start_time.month,
                                                  search_start_time.day, 00,
                                                  00, 00)
            search_end_time = datetime.datetime.strptime(search_end_time, '%Y-%m-%d')
            search_end_time = datetime.datetime(search_end_time.year, search_end_time.month, search_end_time.day, 23,
                                                59, 59)
    today = datetime.datetime.now()
    # search_today = today
    # search_tomorrow = today
    # search_today = datetime.datetime(search_today.year, search_today.month, search_today.day, 00, 00, 00)
    # search_today_end = datetime.datetime(search_tomorrow.year, search_tomorrow.month, search_tomorrow.day, 23, 59, 59)
    message = video_flow.objects.filter(start_date__range=(search_start_time, search_end_time)).order_by('start_date')

    return render_to_response('FAQform.html', {'message': message, 'today': today, })


def cgtn_flow_list(request):
    if request.method == 'GET':
        search_start_time = request.GET.get('starttime')
        search_end_time = request.GET.get('endtime')
        search_field = request.GET.get('searchfield')
        if search_field:
            search_end_time = str(search_end_time)
            search_start_time = str(search_start_time)
            search_field = int(search_field)
            search_start_time = datetime.datetime.strptime(search_start_time, '%Y-%m-%d')
            search_start_time = datetime.datetime(search_start_time.year, search_start_time.month,
                                                  search_start_time.day, 00,
                                                  00, 00)
            search_end_time = datetime.datetime.strptime(search_end_time, '%Y-%m-%d')
            search_end_time = datetime.datetime(search_end_time.year, search_end_time.month, search_end_time.day, 23,
                                                59, 59)
        if search_field == 0:
            message = cgtn_flow.objects.filter(plan_start_date__range=(search_start_time, search_end_time))
        elif search_field == 1:
            message = cgtn_flow.objects.filter(updata_time__range=(search_start_time, search_end_time))
        else:
            today = datetime.datetime.now()
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            search_today = today
            search_today = datetime.datetime(search_today.year, search_today.month, search_today.day, 00, 00, 00)
            search_today_end = datetime.datetime(search_today.year, search_today.month, search_today.day, 23, 59, 59)
            search_tomorrow = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59)
            message = cgtn_flow.objects.filter(plan_start_date__range=(search_today, search_tomorrow))
            message_count = cgtn_flow.objects.filter(
                plan_start_date__range=(search_today, search_today_end)).aggregate(Count('id'))
            search_start_time = today
            search_end_time = tomorrow
    message_count = message.aggregate(Count('id'))
    return render_to_response('cgtn_flow_list_new.html',
                              {'message': message, 'message_count': message_count, 'today': search_start_time,
                               'tomorrow': search_end_time, 'search_field': search_field})



    # today = datetime.datetime.now()
    # tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    # search_today = today
    # search_today = datetime.datetime(search_today.year, search_today.month, search_today.day, 00, 00, 00)
    # search_today_end = datetime.datetime(search_today.year, search_today.month, search_today.day, 23, 59, 59)
    # search_tomorrow = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59)
    # message = cgtn_flow.objects.filter(plan_start_date__range=(search_today, search_tomorrow))
    # message_count = cgtn_flow.objects.filter(plan_start_date__range=(search_today, search_today_end)).aggregate(
    #     Count('id'))
    # return render_to_response('cgtn_flow_list_new.html',
    #                           {'message': message, 'message_count': message_count, 'today': today,
    #                            'tomorrow': tomorrow})
def cgtn_log(request):
    if request.method == 'GET':
        program_type = {
            'cgtne':'cctve_fb',
            'cgtna': 'cctva_fb',
            'cgtnr': 'cctvr_fb',
            'cgtnf': 'cctvf_fb',
            'cgtnelive': 'cctve_live_fb',
            'cgtnalive': 'cctva_live_fb',
            'cgtnrlive': 'cctvr_live_fb',
            'cgtnflive': 'cctvf_live_fb',

        }
        log_tag = request.GET.get('program')
        log_stram = cgtn_control.objects.get(cgtn_type=program_type[log_tag])
        search_rtmp = log_stram.cgtn_flow_rtmp
        envconf = open(os.path.join(os.path.dirname(__file__), 'srs.server.conf'), mode='r')
        envdict = {}
        for line in envconf:
            envdict[line.split()[0]] = line.split()[1]
        envconf.close()
        env.host_string = envdict['host']
        env.port = envdict['port']
        env.user = envdict['user']
        env.password = envdict['password']
        envsu = envdict['sudo_user']
        envpass = envdict['sudo_password']
        logName = 'cat /usr/local/srs2.0/objs/*' + search_rtmp.split('/')[-1].replace(r'&',r'\&') + '.log'
        print logName
        @task
        def task_getlog():

            with hide('everything'):
                with settings(user=envsu,password=envpass):
                    a = run(logName).stdout
                    return a
        logtext = re.split(r'\n|\r',task_getlog())[-20:]
        for i in range(0,len(logtext)):
            logtext[i] = logtext[i] + '<br>'
        # return render(request, 'log.html', {'logtext': logtext[-10:], })
        return HttpResponse(logtext)
def cgtn_change_unlock(request):
    if request.method == 'POST':
        postdate = {}
        change_cgtn_status={}
        postdate['cctva_fb'] = request.POST.get('cgtna')
        postdate['cctvr_fb'] = request.POST.get('cgtnr')
        postdate['cctve_fb'] = request.POST.get('cgtne')
        postdate['cctvf_fb'] = request.POST.get('cgtnf')
        postdate['cctva_live_fb'] = request.POST.get('cgtnalive')
        postdate['cctvr_live_fb'] = request.POST.get('cgtnrlive')
        postdate['cctve_live_fb'] = request.POST.get('cgtnelive')
        postdate['cctvf_live_fb'] = request.POST.get('cgtnflive')

        for i in postdate:
            if  postdate[i] and 'unlock' in postdate[i] :
                change_cgtn_status[i] = unquote(postdate[i])
        for key in change_cgtn_status:
            change_status_unlock = cgtn_control.objects.filter(cgtn_type = key)
            change_status_unlock.update(cgtn_status=1)
        return HttpResponse('ok')


def cgtn_change(request):
    if request.method == 'GET':
        status = {}
        cgtn_change_input_status = cgtn_control.objects.all()
        for item in cgtn_change_input_status:
            status[item.cgtn_type] = [item.cgtn_status, item.cgtn_flow_rtmp]

        return render(request,'cgtn_flow_change.html',status)
    elif request.method == 'POST':
        #get the post data and init the postdict
        # for i in request.POST:
        #     print i
        # print request.POST.get('cgtnf')
        postdate={}
        postdate['cctva_fb'] = request.POST.get('cgtna')
        postdate['cctvr_fb'] = request.POST.get('cgtnr')
        postdate['cctve_fb'] = request.POST.get('cgtne')
        postdate['cctvf_fb'] = request.POST.get('cgtnf')
        postdate['cctva_live_fb'] = request.POST.get('cgtnalive')
        postdate['cctvr_live_fb'] = request.POST.get('cgtnrlive')
        postdate['cctve_live_fb'] = request.POST.get('cgtnelive')
        postdate['cctvf_live_fb'] = request.POST.get('cgtnflive')
        # init the context,this is not need any more

        envconf = open(os.path.join(os.path.dirname(__file__), 'srs.server.conf'),mode='r')
        envdict={}
        for line in envconf:
            envdict[line.split()[0]] = line.split()[1]
        envconf.close()
        env.host_string = envdict['host']
        env.port = envdict['port']
        env.user = envdict['user']
        envsu = envdict['sudo_user']
        envpass = envdict['sudo_password']

        local_srsconf = os.path.join(os.path.dirname(__file__), 'srs.conf')

        localfile_path = local_srsconf

        remotefile_path = '/usr/local/srs2.0/conf/srs.conf'

        # read the default file
        change_rtmp_dict = {}
        # srs_default = os.path.join(os.path.dirname(__file__),'srs_default')
        # srs_obj = open(srs_default, mode='r')
        # for line in srs_obj:
        #     if not line:
        #         break
        #     list = re.split(' ', line)
        #     if len(list) > 1:
        #         change_rtmp_dict[list[0]] = list[1]
        # srs_obj.close()
        # get the link from web,and change the dict list
        for i in postdate:
            if  postdate[i] and 'rtmp://' in postdate[i] :
                change_rtmp_dict[i] = unquote(postdate[i])
        for i in change_rtmp_dict:
            if len(change_rtmp_dict[i])>10:
                change_status = cgtn_control.objects.filter(cgtn_type=i)
                print change_status.values('cgtn_flow_rtmp')
                if change_rtmp_dict[i] == change_status.values('cgtn_flow_rtmp')[0]['cgtn_flow_rtmp']:
                    return redirect('/list/cgtnchange')
                change_status.update(cgtn_flow_rtmp=change_rtmp_dict[i],cgtn_status=0)

        # change the srs server conf file,must read the remote server conf first,then change the text file
        @task
        def get_remote_conf():
            with settings(user=envsu, password=envpass):
                get(remotefile_path,localfile_path)
        get_remote_conf()

        cgtn_read_conf = open(localfile_path,mode='r+')
        # for line in cgtn_context:
        #     for k,v in change_rtmp_dict.items():
        #         if k in line:
        #             line =v
        # cgtn_context.close()
        # cgtn_file = open(local_srsconf, mode='w')
        # cgtn_file.write(cgtn_context)
        #cgtn_file.close()

        conf_context = cgtn_read_conf.readlines()
        isinput = False
        dict_name = ''
        for i in range(0, len(conf_context)):
            for key in change_rtmp_dict:
                if key in conf_context[i]:
                    isinput = True
                    dict_name=key
            if isinput and 'output' in conf_context[i]:
                conf_context[i]='            output          ' + change_rtmp_dict[dict_name] + ';\n'
                isinput = False
        cgtn_read_conf.close()

        cgtn_write_conf = open(localfile_path,mode='w')
        for i in conf_context:
            cgtn_write_conf.write(i)
        cgtn_write_conf.close()
        # save the  changes
        # srs_obj_save = open(srs_default, mode='w')
        # for k, v in change_rtmp_dict.items():
        #     if '\n' in v:
        #         line = k + ' ' + v
        #     else:
        #         line =  k + ' ' + v +'\n'
        #     srs_obj_save.write(line)
        # srs_obj_save.close()

        # backup the source conf file , the form should be name and date ,make sure if some error cause ,the admin can recover the server


        @task
        def task_backup_conf():
            with settings(user=envsu, password=envpass):
                todaytime = datetime.datetime.now().strftime('%y%m%d')
                #timestamp = todaytime + 'c00'
                #remotefile_path_stamp = remotefile_path+timestamp
                check_files_comm = 'ls ' + remotefile_path[0:-8]
                check_files = run(check_files_comm).split()
                searchconf = '^srs.conf' + todaytime +'c\d\d'

                compar_num=0
                for confi in check_files:
                    if re.search(searchconf,confi):
                        if compar_num < int(confi[-2:]):
                            compar_num = int(confi[-2:])
                compar_num+=1
                if compar_num <10 :
                    compar_num = '0'+str(compar_num)
                else:
                    compar_num = str(compar_num)
                # print check_files.split()
                # if exists(remotefile_path_stamp):
                #     remotefile_path_stamp = 1
                # else:
                #     remotefile_path_stamp = remotefile_path + timestamp + 'c00'
                backcomm = 'cp ' + remotefile_path + ' ' + remotefile_path +todaytime+'c'+compar_num
                run(backcomm)

        # upload the change file,a PYer suggest me to use  fabric to implement the features,in the past i used to
        # use paramiko packet to do this ,may be i can change to use this one, let me try

        @task
        def task_upload_file():
            with settings(user=envsu, password=envpass):
                put(localfile_path, remotefile_path)

        # check the file MD5 , if file block reload .check the privileges make sure the file has the right permit.

        @task
        def task_check_md5():
            with settings(user=envsu, password=envpass):
                md5comm = 'md5sum ' + localfile_path
                localmd5 = local(md5comm, capture=True).split(' ')[0]
                md5comm = 'md5sum ' + remotefile_path
                remotemd5 = run(md5comm).split(' ')[0]
                return localmd5 == remotemd5

        # restart the process

        @task
        def task_restart_process():
            with settings(user=envsu, password=envpass):
                # run("/etc/init.d/srs reload")
                run("/etc/init.d/srs reload")
                #run('echo /ect/init.d/srsreload')
            # check the process log and show in the front web
        task_backup_conf()

        while True:
            if task_check_md5():
                task_restart_process()
                time.sleep(1)
                break
            else:
                task_upload_file()
        return render(request,'cgtn_flow_change.html')


def cgtn_log_change(request):
    envconf = open(os.path.join(os.path.dirname(__file__), 'srs.server.conf'), mode='r')
    envdict = {}
    for line in envconf:
        envdict[line.split()[0]] = line.split()[1]
    envconf.close()
    env.host_string = envdict['host']
    env.user = envdict['user']
    env.password = envdict['password']
    localfile_path = os.path.join(os.path.dirname(__file__), 'srs.conf')


    remotefile_path = '/usr/local/srs2.0/conf/srs.conf'
    if request.method=='GET':
        status = {}
        cgtn_change_input_status = cgtn_control.objects.all()
        for item in cgtn_change_input_status:
            status[item.cgtn_type]=[item.cgtn_status,item.cgtn_flow_rtmp]
        return
    return


def cgtnexport(request):
    if request.method == 'GET':
        search_start_time = request.GET.get('starttime')
        search_end_time = request.GET.get('endtime')
        if search_start_time:
            search_end_time = str(search_end_time)
            search_start_time = str(search_start_time)
            search_start_time = datetime.datetime.strptime(search_start_time, '%Y-%m-%d')
            search_start_time = datetime.datetime(search_start_time.year, search_start_time.month,
                                                  search_start_time.day, 00,
                                                  00, 00)
            search_end_time = datetime.datetime.strptime(search_end_time, '%Y-%m-%d')
            search_end_time = datetime.datetime(search_end_time.year, search_end_time.month, search_end_time.day, 23,
                                                59, 59)
            message = cgtn_flow.objects.filter(plan_start_date__range=(search_start_time, search_end_time))
            activity_list = message.aggregate(Count('id'))
            response = HttpResponse(content_type="application/ms-excel")
            response['Content-Disposition'] = 'attachment; filename=file.xls'

            wb = xlwt.Workbook()
            ws = wb.add_sheet('Sheetname')
            icon = 1
            dateFormat = xlwt.XFStyle()
            dateFormat.num_format_str = 'yyyy/mm/dd hh:mm'
            list_taitle=[u'开始时间',u'结束时间',u'需求部门',u'负责人',u'节目名称',u'用途',u'备注']
            for i in range(0,len(list_taitle)):
                ws.write(0,i,list_taitle[i])
            for infor in message:
                plan_start_day =  infor.plan_start_date.replace(tzinfo=None)
                plan_start_day=plan_start_day + datetime.timedelta(hours=8)
                ws.write(icon, 0, plan_start_day,dateFormat)
                plan_end_day = infor.plan_end_date.replace(tzinfo=None)
                plan_end_day = plan_end_day + datetime.timedelta(hours=8)
                ws.write(icon, 1, plan_end_day,dateFormat)
                ws.write(icon, 2, infor.get_department_display())
                ws.write(icon, 3, infor.admin_name)
                ws.write(icon, 4, infor.program_name)
                ws.write(icon, 5, infor.get_use_for_display())
                ws.write(icon, 6, infor.notes)
                icon += 1
            wb.save(response)
            return response

#fangfaer
            # obj = message.first()
            # for y, column in enumerate(columns):
            #     value = get_column_head(obj, column)
            #     sheet.write(0, y, value, header_style)
            #
            # for x, obj in enumerate(queryset, start=1):
            #     for y, column in enumerate(columns):
            #         value = get_column_cell(obj, column)
            #         style = default_style
            #         for value_type, cell_style in cell_style_map:
            #             if isinstance(value, value_type):
            #                 style = cell_style
            #         sheet.write(x, y, value, style)

#fangfayi
            # response = HttpResponse(content_type='application/vnd.ms-excel')
            # response['Content-Disposition'] = 'attachment; filename=reportdata.xls'  # 返回下载文件的名称(activity.xls)
            # workbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
            # mysheet = workbook.add_sheet(u'活动')  # 创建工作页
            # rows = activity_list
            # cols = 10  # 每行的列
            # aaa = ['活动名称', '订单名称', '投放日期', '结束日期', '直播点击数', '直播订阅量', '直播访问量', '开始时间', '结束时间', '广告主名称']  # 表头名
            # for c in range(len(aaa)):
            #     mysheet.write(0, c, aaa[c])
            # for r in range(0, len(rows)):  # 对行进行遍历
            #     for c in range(cols):  # 对列进行遍历
            #         mysheet.write(r + 1, c, str(rows[r][c]))
            #         response = HttpResponse(
            #             content_type='application/vnd.ms-excel')  # 这里响应对象获得了一个特殊的mime类型,告诉浏览器这是个excel文件不是html
            #         response[
            #             'Content-Disposition'] = 'attachment; filename=reportdata.xls'  # 这里响应对象获得了附加的Content-Disposition协议头,它含有excel文件的名称,文件名随意,当浏览器访问它时,会以"另存为"对话框中使用它.
            #         workbook.save(response)
            # return response

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
