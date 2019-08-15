from django.shortcuts import render, redirect
from configureBaseData.models.suppliers import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from excelTrigger.readSuppliersPrograms import syncTable
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def listAllSuppliers(request):
    targId = request.GET.get('sid')
    print(targId)
    if targId:
        result = SupplyProgram.objects.filter(vender__id=targId).values('programname', 'vender__id', 'programtype',
                                                                       'vender__chinaname', 'note', 'vender', 'height',
                                                                       'width', 'bandwidth', 'inPutType', 'inPutStream')
    else:
        result = SupplyProgram.objects.all().values('programname', 'vender__id', 'programtype',
                                                    'vender__chinaname', 'note', 'vender', 'height',
                                                    'width', 'bandwidth', 'inPutType', 'inPutStream')
    paginator = Paginator(result, 30)
    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return render(request, 'suppliers/listall.html', {'result': result})


@login_required
def SuppliersDetail(request):
    targetId = request.GET.get('id')
    result = VideoSupplier.objects.filter(id=targetId).values('chinaname', 'englishname', 'note')
    resultStaff = SupplierStaff.objects.filter(company=targetId)
    return render(request, 'suppliers/suppliersdetail.html', {'result': result, 'resultStaff': resultStaff})


@login_required
def inportSuppliersExcel(request):
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
        getInportObj = syncTable(filepath=file_path, filename=obj.name)
        getInportObj.writetodb()
        return redirect('/suppliers/listall/')
    elif request.method == 'GET':
        return render(request, 'suppliers/inportexcel.html')
