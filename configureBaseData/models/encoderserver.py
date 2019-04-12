from django.db import models
from django.utils import timezone
from configureBaseData.models.devices import Machine
from configureBaseData.models.businesses import Business
import datetime
from ..configureChoices import *


class ProgramDetail(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True)
    rowid = models.IntegerField(null=True)
    name = models.CharField(max_length=255)
    switchStatus = models.BooleanField(default=False)
    programStatus = models.IntegerField(default=-1)
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
    taskName = models.CharField(verbose_name='任务名称', max_length=255)
    startDate = models.DateTimeField(verbose_name='计划开始时间', blank=True, null=True)
    endDate = models.DateTimeField(verbose_name='计划结束时间', blank=True, null=True)
    typeOf = models.CharField(verbose_name='任务类型', choices=typeOfTaskChoices, max_length=255)

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
    programStatus = models.IntegerField(verbose_name='频道状态', blank=True, default=0)
    programName = models.CharField(verbose_name='节目名称', max_length=255, )
    inPutStream = models.CharField(verbose_name='源地址', max_length=255, )
    isLive = models.BooleanField(verbose_name='直播', default=False, blank=True)
    isRecode = models.BooleanField(verbose_name='收录', default=False, blank=True)
    notes = models.TextField(verbose_name='备注', null=True, blank=True)
    adminStaff = models.ForeignKey('Staff', on_delete=None, blank=True, default=None)

    def __str__(self):
        return self.programName

    class Meta:
        verbose_name = '工作包'
        verbose_name_plural = '工作包'


class Staff(models.Model):
    task = models.ManyToManyField(Task, blank=True, )
    department = models.CharField(verbose_name='需求部门', choices=departmentChoices, blank=True, max_length=30)
    staffName = models.CharField(verbose_name='负责人', blank=True, max_length=30)
    phoneNumber = models.IntegerField(verbose_name='电话', blank=True)
    note = models.CharField(verbose_name='备注', blank=True, null=True, max_length=60)

    class Meta:
        verbose_name = '业务人员'
        verbose_name_plural = '业务人员'

    def __str__(self):
        return self.staffName
