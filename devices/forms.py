from django import forms
from configureBaseData.configureChoices import *
from configureBaseData.models.encoderserver import Staff


class ProgramDetailForm(forms.Form):
    machine = forms.IntegerField()
    rowid = forms.IntegerField()
    name = forms.CharField(max_length=255)
    switchStatus = forms.BooleanField()
    programStatus = forms.IntegerField()
    height = forms.IntegerField()
    width = forms.IntegerField()
    outbandwidth = forms.IntegerField()
    inPutFirst = forms.CharField(max_length=255, )
    inPutSecond = forms.CharField(max_length=255, )
    outPutFirst = forms.CharField(max_length=255, )
    outPutSecond = forms.CharField(max_length=255, )
    outPutHttpFlow = forms.URLField()


class TaskForm(forms.Form):
    taskName = forms.CharField(max_length=255)
    startDate = forms.DateTimeField(required=True,
                                    input_formats=['%Y-%m-%d'],
                                    widget=forms.DateTimeInput(attrs={
                                        'class': 'form-control datetimepicker-input',
                                        'data-target': '#datetimepicker1'
                                    })
                                    )
    endDate = forms.DateTimeField(required=True,
                                  input_formats=['%Y-%m-%d'],
                                  widget=forms.DateTimeInput(attrs={
                                      'class': 'form-control datetimepicker-input',
                                      'data-target': '#datetimepicker2'
                                  })
                                  )
    typeOf = forms.ChoiceField(choices=typeOfTaskChoices, required=True, )


def choiceAdminStaff():
    choice = forms.ChoiceField(choices=[
        (choice.pk, choice) for choice in Staff.objects.all()])
    return choice


class WorkPackageForm(forms.Form):
    task = forms.IntegerField()
    startDate = forms.DateTimeField(required=True,
                                    input_formats=['%d/%m/%Y %H:%M'],
                                    widget=forms.DateTimeInput(attrs={
                                        'class': 'form-control datetimepicker-input',
                                        'data-target': '#datetimepicker1'}))
    endDate = forms.DateTimeField(required=True,
                                  input_formats=['%d/%m/%Y %H:%M'],
                                  widget=forms.DateTimeInput(attrs={
                                      'class': 'form-control datetimepicker-input',
                                      'data-target': '#datetimepicker2'}))
    programChannel = forms.ChoiceField(choices=programChannelChoices)
    # programStatus = forms.IntegerField()
    programName = forms.CharField(max_length=255, )
    inPutStream = forms.CharField(max_length=255, )
    isLive = forms.BooleanField(widget=forms.CheckboxInput(), required=False, )
    isRecode = forms.BooleanField(widget=forms.CheckboxInput(), required=False, )
    notes = forms.CharField()
    adminStaff = forms.ModelChoiceField(queryset=Staff.objects.all())


class StaffForm(forms.Form):
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
    # task = forms.ManyToManyField(Task,  )
    department = forms.CharField(max_length=30)
    staffName = forms.CharField(max_length=30)
