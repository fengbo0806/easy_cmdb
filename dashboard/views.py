from django.shortcuts import render


# Create your views here.
def dashboard(request):
    return render(request, 'basic.html')


def mainboard(request):
    return render(request, 'dashboard/maindashboard.html')
