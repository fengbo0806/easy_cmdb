from django.db import models
from django.utils import timezone
from configureBaseData.models.devices import Machine
from configureBaseData.models.businesses import Business
import datetime


class ProgramDetail(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, )
    rowid = models.IntegerField()
    name = models.CharField(max_length=255)
    switchStatus = models.BooleanField()
    programStatus = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    outbandwidth = models.IntegerField()
    inPutFirst = models.CharField(max_length=255, null=True, blank=True)
    inPutSecond = models.CharField(max_length=255, null=True, blank=True)
    outPutFirst = models.CharField(max_length=255, null=True, blank=True)
    outPutSecond = models.CharField(max_length=255, null=True, blank=True)
    outPutHttpFlow = models.URLField()

    def __str__(self):
        return str(self.name)

    class Meta:
        unique_together = ('machine', 'rowid',)
        verbose_name = '频道表'
        verbose_name_plural = '频道表'


class Task(models.Model):
    typeOfTask = (
        ('项目型', '项目型'),
        ('运营型', '运营型'),
    )
    taskName = models.CharField(verbose_name='任务名称', max_length=255)
    startDate = models.DateTimeField(verbose_name='计划开始时间', blank=True, null=True)
    endDate = models.DateTimeField(verbose_name='计划结束时间', blank=True, null=True)
    typeOf = models.CharField(verbose_name='任务类型',choices=typeOfTask,max_length=255)

    def __str__(self):
        return self.taskName

    class Meta:
        verbose_name = '保障任务'
        verbose_name_plural = '保障任务'


class WorkPackage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    startDate = models.DateTimeField(verbose_name='实际开始时间', blank=True, null=True)
    endDate = models.DateTimeField(verbose_name='实际结束时间', blank=True, null=True)
    programChannel = models.CharField(verbose_name='频道名称', max_length=255, )
    programStatus = models.IntegerField(verbose_name='频道状态', )
    programName = models.CharField(verbose_name='节目名称', max_length=255, )
    inPutStream = models.CharField(verbose_name='源地址', max_length=255, )
    isLive = models.BooleanField(verbose_name='直播')
    isRecode = models.BooleanField(verbose_name='收录')
    notes = models.TextField(verbose_name='备注', null=True, blank=True)
    adminStaff = models.ForeignKey('Staff', on_delete=None, blank=True, default=None)

    def __str__(self):
        return self.programName

    class Meta:
        verbose_name = '工作包'
        verbose_name_plural = '工作包'


class Staff(models.Model):
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
    task = models.ManyToManyField(Task, blank=True, )
    department = models.CharField(verbose_name='需求部门', choices=department, blank=True, max_length=30)
    staffName = models.CharField(verbose_name='负责人', blank=True, max_length=30)

    class Meta:
        verbose_name = '业务人员'
        verbose_name_plural = '业务人员'

    class Meta:
        verbose_name = '业务人员'
        verbose_name_plural = '业务人员'
