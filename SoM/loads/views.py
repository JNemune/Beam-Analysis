from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def ForceLoad(request):
    if request.method == 'POST':
        cd = request.POST
        yMagnitude = cd['yMag']
        xMagnitude = cd['xMag']
        start = float(cd['Start'])
        stop = float(cd['Stop'])

        if cd['yunit'] == 'kips':
            yMagnitude = f'({yMagnitude})*4.448'

        if cd['xunit'] == 'kips':
            xMagnitude = f'({xMagnitude})*4.448'

        type = cd['start_stop']
        if type == 'MM':
            start = start/1000
            stop = stop/1000
        elif type== 'IN':
            start = start*2.54/100
            stop = stop*2.54/100
        elif type == 'FT':
            start = start/3.281
            stop = stop/3.281

        ForceModel.objects.create(x=xMagnitude, y=yMagnitude, x1=start, x2=stop)

    return render(request, 'loads/Force.html')



def MomentLoad(request):
    if request.method == 'POST':
        cd = request.POST
        xMagnitude = cd['xMag']
        zMagnitude = cd['zMag']
        start = float(cd['Start'])
        stop = float(cd['Stop'])

        if cd['xunit'] == 'kips':
            xMagnitude = f'({xMagnitude})*4.448'

        if cd['zunit'] == 'kips':
            zMagnitude = f'({zMagnitude})*4.448'

        type = cd['start_stop']
        if type == 'MM':
            start = start/1000
            stop = stop/1000
        elif type== 'IN':
            start = start*2.54/100
            stop = stop*2.54/100
        elif type == 'FT':
            start = start/3.281
            stop = stop/3.281

        MomentModel.objects.create(x=xMagnitude, z=zMagnitude, x1=start, x2=stop)

    return render(request, 'loads/Moment.html')

def ClearForce(request):
    ForceModel.objects.all().delete()
    return redirect('home')

def ClearMoment(request):
    MomentModel.objects.all().delete()
    return redirect('home')