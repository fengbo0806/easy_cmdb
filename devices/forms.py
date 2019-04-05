from django import forms


class ProgramDetail(forms.Form):
    machine = forms.IntegerField(null=True)
    rowid = forms.IntegerField(null=True)
    name = forms.CharField(max_length=255)
    switchStatus = forms.BooleanField()
    programStatus = forms.IntegerField()
    height = forms.IntegerField()
    width = forms.IntegerField()
    outbandwidth = forms.IntegerField()
    inPutFirst = forms.CharField(max_length=255, null=True, blank=True)
    inPutSecond = forms.CharField(max_length=255, null=True, blank=True)
    outPutFirst = forms.CharField(max_length=255, null=True, blank=True)
    outPutSecond = forms.CharField(max_length=255, null=True, blank=True)
    outPutHttpFlow = forms.URLField()


class Task(forms.Form):
    typeOfTask = (
        ('项目型', '项目型'),
        ('运营型', '运营型'),
    )
    taskName = forms.CharField(verbose_name='任务名称', max_length=255)
    startDate = forms.DateTimeField(verbose_name='计划开始时间', blank=True, null=True)
    endDate = forms.DateTimeField(verbose_name='计划结束时间', blank=True, null=True)
    typeOf = forms.CharField(verbose_name='任务类型', choices=typeOfTask, max_length=255)


class WorkPackage(forms.Form):
    task = forms.IntegerField()
    startDate = forms.DateTimeField(verbose_name='实际开始时间', blank=True, null=True)
    endDate = forms.DateTimeField(verbose_name='实际结束时间', blank=True, null=True)
    programChannel = forms.CharField(verbose_name='频道名称', max_length=255, )
    programStatus = forms.IntegerField(verbose_name='频道状态', )
    programName = forms.CharField(verbose_name='节目名称', max_length=255, )
    inPutStream = forms.CharField(verbose_name='源地址', max_length=255, )
    isLive = forms.BooleanField()
    isRecode = forms.BooleanField()
    notes = forms.CharField(verbose_name='备注', null=True, blank=True)
    adminStaff = forms.IntegerField(blank=True, default=None)


class Staff(forms.Form):
    department = (
        ('体育中心', '体育中心'),
        ('微视频工作室', '微视频工作室'),
        ('少儿社区部', '少儿社区部'),
        ('央视新闻', '央视新闻'),
        ('综艺社区部', '综艺社区部'),
        ('网络媒体事业部', '网络媒体事业部'),
        ('品牌部', '品牌部'),
        ('国际传播事业部', '国际传播事业部'),
        ('舆论场', '舆论场'),
        ('CGTN', 'CGTN'),
        ('科教纪录中心', '科教纪录中心'),
    )
    # task = forms.ManyToManyField(Task, blank=True, )
    department = forms.CharField(verbose_name='需求部门', choices=department, blank=True, max_length=30)
    staffName = forms.CharField(verbose_name='负责人', blank=True, max_length=30)
