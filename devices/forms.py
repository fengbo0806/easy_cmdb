from django import forms
from configureBaseData.configureChoices import *
from configureBaseData.models.encoderserver import Staff
from configureBaseData.models.devices import MachineRoom,MachineRack


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
    # task = forms.ManyToManyField(Task,  )
    department = forms.ChoiceField(choices=departmentChoices)
    staffName = forms.CharField(max_length=30)
    phoneNumber = forms.IntegerField(required=False)
    note = forms.CharField(required=False)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


'''
machine rooms
'''


class MachineRoomForm(forms.Form):
    '''
    describ the address of IDC, maybe some detail information for contant of the service stuff
    '''
    name = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    note = forms.CharField(max_length=255)


class MachineRackForm(forms.Form):
    '''
    describe the detail maching rack locate
    '''
    floor = forms.IntegerField()
    locate = forms.CharField(max_length=30)
    note = forms.CharField(max_length=30)
    room = forms.ModelChoiceField(queryset=MachineRoom.objects.all(), )


class MachineLocateForm(forms.Form):
    '''
    describe the macing locate
    '''
    Ulocate = forms.IntegerField()
    rack = forms.ModelChoiceField(queryset=MachineRack.objects.all(), )
