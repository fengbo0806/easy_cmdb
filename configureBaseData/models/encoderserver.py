from django.db import models
from django.utils import timezone
from configureBaseData.models.devices import Machine
from configureBaseData.models.businesses import Business
import datetime


class ProgramDetail(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, )
    rowid = models.IntegerField()
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    outbandwidth = models.IntegerField()

    def __str__(self):
        return str(self.name)
    class Meta:
        unique_together = ('machine', 'rowid',)



class Task(models.Model):
    taskName=models.CharField(verbose_name='任务名称',max_length=255)
    startDate = models.DateTimeField(verbose_name='计划开始时间', blank=True, null=True)
    endDate = models.DateTimeField(verbose_name='计划结束时间', blank=True, null=True)


class WorkPackage(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE)
    startDate = models.DateTimeField(verbose_name='实际开始时间', blank=True, null=True)
    endDate = models.DateTimeField(verbose_name='实际结束时间', blank=True, null=True)
    programChannel= models.CharField(verbose_name='频道名称',max_length=255,)
    programName= models.CharField(verbose_name='节目名称',max_length=255,)
    class Meta:
        verbose_name = '工作包'
        verbose_name_plural = '工作包'

class Staff(models.Model):
    department=(
        ('0','体育中心'),
        ('1','微视频工作室'),
        ('2','少儿社区部'),
        ('3','央视新闻'),
        ('4','综艺社区部'),
        ('5','网络媒体事业部'),
        ('6','品牌部'),
        ('7','国际传播事业部'),
        ('8','舆论场'),
        ('9','CGTN'),
        ('10', '科教纪录中心'),
    )
    task = models.ManyToManyField(Task,blank=True, null=True)
    department = models.CharField(verbose_name='需求部门', choices=department, blank=True, max_length=30)
    staffName = models.CharField(verbose_name='负责人', blank=True, max_length=30)
