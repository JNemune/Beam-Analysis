from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BeamForm
from .models import BeamModel, SupportModel


def beam_creator(request):
    if request.method == 'POST':
        cd = request.POST
	
        length= float(cd['len'])
        unit_1=cd['unit1']
        F = float(cd['F'])
        FT = float(cd['FT'])
        W = float(cd['W'])
        WT = float(cd['WT'])
        unit_2=cd['unit2']

        if unit_1 == 'MM':
            length = length/1000
        elif unit_1 == 'IN':
            length = length*2.54/100
        elif unit_1 == 'FT':
            length = length/3.281

        if unit_2 == 'MM':
            F = F/1000
            FT = FT/1000
            W = W/1000
            WT = WT/1000
        elif unit_2 == 'IN':
            F = F*2.54/100
            FT = FT*2.54/100
            W = W*2.54/100
            WT = WT*2.54/100
        elif unit_2 == 'FT':
            F = F/3.281
            FT = FT/3.281
            W = W/3.281
            WT = WT/3.281

        BeamModel.objects.create(
                len=length,
                unit_1=cd['unit1'],
                f = F,
                ft = FT,
                w = W,
                wt = WT,
                unit_2=cd['unit2']
        )
    return redirect('beam')


def support_type(request):
    if request.method == 'POST':
        cd = request.POST
        type = cd['type']
        return render(request, 'model/support.html', {'type':type})
    else:
        return render(request, 'model/support.html', {'type':None})
    

def cantilevered(request):
    if request.method == 'POST':
        cd = request.POST
        len = float(cd['Can'])
        if cd['unit'] == 'MM':
            xpin = len/1000
        elif cd['unit'] == 'IN':
            xpin = len*2.54/100
        elif cd['unit'] == 'FT':
            xpin = len/3.281
        else:
            xpin = len

        SupportModel.objects.create(a = xpin, b=-1)

    return render(request, 'model/support.html')


def pinroller(request):
    if request.method == 'POST':
        cd = request.POST
        pin = float(cd['Pin'])
        if cd['unit_a'] == 'MM':
            xpin = pin/1000
        elif cd['unit_a'] == 'IN':
            xpin = pin*2.54/100
        elif cd['unit_a'] == 'FT':
            xpin = pin/3.281
        else:
            xpin = pin

        rol = float(cd['Rol'])
        if cd['unit_b'] == 'MM':
            xroller = rol/1000
        elif cd['unit_b'] == 'IN':
            xroller = rol*2.54/100
        elif cd['unit_b'] == 'FT':
            xroller = rol/3.281
        else:
            xroller = rol

        SupportModel.objects.create(a =xpin, b = xroller)
    return render(request, 'model/support.html')
